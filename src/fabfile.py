# coding: utf-8
import os, sys
import re, codecs
import argparse
import paramiko
from fabric.api import *
from fabric.colors import *

from logging import getLogger, StreamHandler, INFO, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

env.use_ssh_config = True
env.mysql_user = os.getenv("MYSQL_USER")
env.mysql_password = os.getenv("MYSQL_PASSWORD")
env.mysql_database_name = os.getenv("MYSQL_DB_NAME")

def webserver_deploy():
  logger.info("## webserver_deploy() exec")
  run("hostname")

def exec_sql_sample():
  logger.info("## exec_sql_sample() exec")
  run("hostname")
  result = mysql_exec(env, "SELECT * FROM table_name", to_array=True)

def mysql_exec(env, mysql_command, to_array=False):
  with shell_env(MYSQL_PWD=env.mysql_password):
    result = run('mysql --batch -u %s -N %s -e "%s"' % (env.mysql_user, env.mysql_database_name, mysql_command), pty=True)
  if to_array: return mysql_result_to_array(result)
  return result

def mysql_result_to_array(targer_arr):
  lines = targer_arr.split('\n')
  
  result = []
  for line in lines:
    result.append(line.split("\t"))
  logger.debug("mysql_result_to_array() result")
  logger.debug(result)
