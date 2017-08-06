import os
import boto3
import logging
import json
import datetime
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# origin の設定 (チェックしない場合、任意のドメインからレポートを送り放題になってしまう)
origin_domain = "example.com"
# Kinesis Firehose の Delivery Stream 名
firehose_stream_name = "csp-report"

firehose = boto3.client('firehose')

def lambda_handler (event, context):
  logger.info(event)
  result = {"report-created": False}

  # POST されたデータが CSP Report かのチェック
  if "csp-report" not in event["body-json"] or "origin" not in event["params"]["header"]:
     logger.info("Invalid CSP Report Request")
     return result

  # 分析に必要な情報を付加して Firehose に POST
  if origin_domain in event["params"]["header"]["origin"]:
    resp = event["body-json"]
    contexts = {
      "User-Agent": event["context"]["user-agent"],
      "SourceIP": event["context"]["source-ip"],
      "Timestamp": datetime.datetime.today().isoformat()
    }
    if "X-Forwarded-For" in event["params"]["header"]:
      contexts["SourceIP"] = event["params"]["header"]["X-Forwarded-For"]

    resp.update(contexts)
    result = json.dumps(resp)

    try:
      response = firehose.put_record(
        DeliveryStreamName = firehose_stream_name,
        Record = {
          'Data': result
        }
      )
      logger.info(response)
      return result

    except Exception as e:
      logger.error(e)
      raise e
      return result

  return result
