import base64
import hashlib
import json
import os.path
import re
import requests
import sys
import webbrowser
import xml.etree.cElementTree as ET
import yaml
import zlib

from datetime import datetime
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urljoin
from buildtest.defaults import BUILD_REPORT
from buildtest.utils.file import resolve_path
from buildtest.utils.tools import deep_get


def cdash_cmd(args, configuration):

    # Shown below is an example cdash setting in configuration file
    #     cdash:
    #       url: https://my.cdash.org
    #       project: buildtest
    #       site: laptop
    cdash_config = deep_get(configuration.target_config, "cdash")

    if not cdash_config:
        sys.exit(f"We found no 'cdash' setting set in configuration file: {configuration.file}. Please specify 'cdash' setting in order to use 'buildtest cdash' command")

    if args.cdash == "view":
        # if url is specified on command line (buildtest cdash view --url) then open link as is
        if args.url:
            webbrowser.open(args.url)
            return


        url = cdash_config["url"]
        project = cdash_config["project"]
        target_url = urljoin(url, f"index.php?project={project}")

        print("URL:",  target_url)
        # check for url via requests, it can raise an exception if its invalid URL in that case we print a message
        try:
            r = requests.get(target_url)
        except requests.ConnectionError as err:
            print(err)

            print("\nShown below is the CDASH settings from configuration file:", configuration.file)
            print(yaml.dump(cdash_config,indent=2))
            sys.exit(f"Invalid URL: {target_url}")

        # A 200 status code is valid URL, if its not found we exit before opening page in browser
        if not r.status_code == 200:
            sys.exit("Invalid URL")

        webbrowser.open(target_url)

    if args.cdash == "upload":

        upload_test_cdash(cdash_config,
            args.site, args.buildname, args.report_file, configuration
        )


def upload_test_cdash(cdash_setting, site, buildname, report_file, configuration):
    """This method is responsible for reading report file and pushing results to CDASH
    server. User can specify cdash settings in configuration file or pass them in command line.
    The command ``buildtest cdash upload`` will upload results to CDASH.

    :param cdash_setting: cdash settings loaded from configuration file
    :type cdash_setting: dict
    :param site: site name that shows up in CDASH
    :type site: str
    :param buildname: build name that shows up in CDASH
    :type site: str
    :param report_file: Path to report file when uploading results. This is specified via ``buildtest cdash upload -r`` command
    :type report_file: str
    :param configuration: Instance of BuildTestConfiguration class that contains the configuration file
    :type configuration: BuildTestConfiguration
    :return:
    """


    cdash_url = cdash_setting["url"]
    project_name = cdash_setting["project"]
    site_name = site or cdash_setting["site"]
    build_name = buildname or cdash_setting["buildname"]


    if not site_name:
        sys.exit("Please specify site name")

    if not build_name:
        sys.exit("Please specify a buildname")

    if not project_name:
        sys.exit("Please specify a project name in cdash section")

    if not cdash_url:
        sys.exit("Please specify a CDASH url in configuration file or via 'buildtest cdash upload --url'")

    try:
        r = requests.get(cdash_url)
    except requests.ConnectionError as err:
        print("\nShown below is the CDASH settings from configuration file:", configuration.file)
        print(yaml.dump(cdash_config, indent=2))
        sys.exit(err)

    if not requests.get(cdash_url).status_code == 200:
        sys.exit(f"Invalid URL: {cdash_url} please check your CDASH server URL.")

    upload_url = urljoin(cdash_url, f"submit.php?project={project_name}")

    r = requests.get(upload_url)
    # output of text property is the following:
    # '<cdash version="3.0.3">\n  <status>OK</status>\n  <message></message>\n  <md5>d41d8cd98f00b204e9800998ecf8427e</md5>\n</cdash>\n'
    if not re.search("<status>OK</status>", r.text):
        sys.exit(f"Invalid URL: {upload_url}")


    # For best CDash results, builds names should be consistent (ie not change every time).

    input_datetime_format = "%Y/%m/%d %H:%M:%S"
    output_datetime_format = "%Y%m%d-%H%M"

    build_starttime = None
    build_endtime = None

    tests = []
    abspath_report_file = resolve_path(report_file) or BUILD_REPORT
    if not abspath_report_file:
        sys.exit(
            f"Unable to find report file: {report_file} please build a test via buildtest build"
        )

    print("Reading report file: ", abspath_report_file)

    with open(abspath_report_file) as json_file:
        buildtest_data = json.load(json_file)
        for file_name in buildtest_data.keys():
            for test_name, tests_data in buildtest_data[file_name].items():
                test_data = tests_data[0]

                test = {}
                test["name"] = test_name

                state = test_data["state"]
                if state == "PASS":
                    test["status"] = "passed"
                elif state == "FAIL":
                    test["status"] = "failed"
                else:
                    print(
                        "Unrecognized state {0} for test {1}; marking it as failed".format(
                            state, test_name
                        )
                    )
                    test["status"] = "failed"

                test["command"] = test_data["command"]
                test["path"] = test_data["testpath"]
                test["test_content"] = test_data["test_content"]
                test["output"] = test_data["output"]
                test["runtime"] = test_data["runtime"]
                test["returncode"] = test_data["returncode"]
                test["full_id"] = test_data["full_id"]
                test["user"] = test_data["user"]
                test["hostname"] = test_data["hostname"]
                test["schemafile"] = test_data["schemafile"]

                test["tags"] = test_data["tags"]
                test["executor"] = test_data["executor"]
                test["compiler"] = test_data["compiler"]
                test["starttime"] = test_data["starttime"]
                test["endtime"] = test_data["endtime"]

                # extra preformatted output fields
                test["buildspec_content"] = test_data["buildspec_content"]
                test["error"] = test_data["error"]
                test["test_content"] = test_data["test_content"]

                # tags == labels
                test["tags"] = test_data["tags"]

                # ignored for now
                # testroot = test_data['testroot']
                # stagedir = test_data['stagedir']
                # rundir = test_data['rundir']
                # outfile = test_data['outfile']
                # errfile = test_data['errfile']

                # test start and end time.
                starttime = test_data["starttime"]
                test_starttime_datetime = datetime.strptime(
                    starttime, input_datetime_format
                )
                endtime = test_data["endtime"]
                test_endtime_datetime = datetime.strptime(
                    endtime, input_datetime_format
                )
                if not build_starttime or build_starttime > test_starttime_datetime:
                    build_starttime = test_starttime_datetime
                if not build_endtime or build_endtime < test_endtime_datetime:
                    build_endtime = test_endtime_datetime
                tests.append(test)

    build_stamp = build_starttime.strftime(output_datetime_format)
    build_stamp += "-Experimental"

    filename = "Test.xml"
    site_element = ET.Element(
        "Site", Name=site_name, BuildName=build_name, BuildStamp=build_stamp
    )
    testing_element = ET.SubElement(site_element, "Testing")
    ET.SubElement(testing_element, "StartTestTime").text = str(
        round(datetime.timestamp(build_starttime))
    )
    ET.SubElement(testing_element, "EndTestTime").text = str(
        round(datetime.timestamp(build_endtime))
    )

    for test in tests:
        test_element = ET.SubElement(testing_element, "Test", Status=test["status"])
        ET.SubElement(test_element, "Name").text = test["name"]
        ET.SubElement(test_element, "Path").text = test["path"]
        ET.SubElement(test_element, "FullCommandLine").text = test["command"]
        results_element = ET.SubElement(test_element, "Results")

        runtime_measurement = ET.SubElement(
            results_element,
            "NamedMeasurement",
            type="numeric/double",
            name="Execution Time",
        )
        ET.SubElement(runtime_measurement, "Value").text = str(test["runtime"])

        testid_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="Test ID"
        )
        ET.SubElement(testid_measurement, "Value").text = test["full_id"]

        returncode_measurement = ET.SubElement(
            results_element,
            "NamedMeasurement",
            type="numeric/double",
            name="Return Code",
        )
        ET.SubElement(returncode_measurement, "Value").text = str(test["returncode"])

        user_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="User"
        )
        ET.SubElement(user_measurement, "Value").text = test["user"]

        hostname_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="Hostname"
        )
        ET.SubElement(hostname_measurement, "Value").text = test["hostname"]

        executor_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="executor"
        )
        ET.SubElement(executor_measurement, "Value").text = test["executor"]

        tags_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="Tags"
        )
        ET.SubElement(tags_measurement, "Value").text = test["tags"]

        testpath_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="testpath"
        )
        ET.SubElement(testpath_measurement, "Value").text = test["path"]

        starttime_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="starttime"
        )
        ET.SubElement(starttime_measurement, "Value").text = test["starttime"]

        endtime_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="endtime"
        )
        ET.SubElement(endtime_measurement, "Value").text = test["endtime"]

        compiler_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="compiler"
        )
        ET.SubElement(compiler_measurement, "Value").text = test["compiler"]

        schema_measurement = ET.SubElement(
            results_element, "NamedMeasurement", type="text/string", name="schemafile"
        )
        ET.SubElement(schema_measurement, "Value").text = test["schemafile"]

        error_content = ET.SubElement(
            results_element, "NamedMeasurement", type="text/preformatted", name="Error"
        )
        ET.SubElement(error_content, "Value").text = test["error"]

        buildspec_content = ET.SubElement(
            results_element,
            "NamedMeasurement",
            type="text/preformatted",
            name="Buildspec Content",
        )
        ET.SubElement(buildspec_content, "Value").text = test["buildspec_content"]

        test_content = ET.SubElement(
            results_element,
            "NamedMeasurement",
            type="text/preformatted",
            name="Test Content",
        )
        ET.SubElement(test_content, "Value").text = test["test_content"]

        output_measurement = ET.SubElement(results_element, "Measurement")

        base64_zlib_output = base64.b64encode(
            zlib.compress(bytes("".join(test["output"]), "ascii"))
        ).decode("ascii")
        ET.SubElement(
            output_measurement, "Value", encoding="base64", compression="gzip"
        ).text = base64_zlib_output

        gitlab_job_url = os.getenv("CI_JOB_URL")
        if gitlab_job_url is not None:
            gitlab_link_measurement = ET.SubElement(
                results_element,
                "NamedMeasurement",
                type="text/link",
                name="View GitLab CI results",
            )
            ET.SubElement(gitlab_link_measurement, "Value").text = gitlab_job_url

        # Report tags as labels
        labels_element = ET.SubElement(test_element, "Labels")
        for tag in test["tags"].split(" "):
            ET.SubElement(labels_element, "Label").text = tag

    xml_tree = ET.ElementTree(site_element)
    xml_tree.write(filename)

    # Compute md5 checksum for the contents of this file.
    with open(filename) as xml_file:
        md5sum = hashlib.md5(xml_file.read().encode("utf-8")).hexdigest()

    buildid_regexp = re.compile("<buildId>([0-9]+)</buildId>")
    with open(filename, "rb") as f:
        params_dict = {
            "build": build_name,
            "site": site_name,
            "stamp": build_stamp,
            "MD5": md5sum,
        }
        print("build name: ", build_name)
        print("site: ", site_name)
        print("stamp: ", build_stamp)
        print("MD5SUM:", md5sum)
        encoded_params = urlencode(params_dict)
        url = "{0}&{1}".format(upload_url, encoded_params)
        hdrs = {"Content-Type": "text/xml", "Content-Length": os.path.getsize(filename)}
        request = Request(url, data=f, method="PUT", headers=hdrs)

        with urlopen(request) as response:
            resp_value = response.read()
            if isinstance(resp_value, bytes):
                resp_value = resp_value.decode("utf-8")
            match = buildid_regexp.search(resp_value)
            print("PUT STATUS:", response.status)
            if match:
                buildid = match.group(1)
                print(f"You can view the results at: {cdash_url}/viewTest.php?buildid={buildid}")