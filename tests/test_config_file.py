import os

def test_answer():
  home_dir = os.getenv("HOME")
  config_file = os.path.join(home_dir,".buildtest/settings.yml")
  assert os.path.isfile(config_file)
