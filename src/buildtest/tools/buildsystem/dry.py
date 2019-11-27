def dry_view(content):
    """Print Content of test script without writting content. This implements ``buildtest build --dry-run``"""
    print(f"Test:{content['testpath']}")
    print("{:-<80}".format(""))
    for k, v in content.items():
        if k == "testpath":
            continue
        print("\n".join(v))
    print("{:-<80}".format(""))
