# webdb100-https-example
このレポジトリは、2017年8月24日発売の[WEB+DB PRESS Vol.100](http://gihyo.jp/magazine/wdpress/archive/2017/vol100)に掲載されている 「対応必須！完全HTTPS化」特集のサンプルコードです。

# サンプルコードの利用方法
レポジトリに含まれるサンプルコードは AWS Lambda で動作し、 Amazon API Gateway のバックエンドとして利用します。
また、レポートの送信は Amazon Kinesis Firehose を用いて、Amazon Elasticsearch Service に格納します。

## 利用方法
### 必要なリソースの作成
1. Amazon Elasticsearch Service において domain を作成します。
2. Amazon Kinesis Firehose の Delivery Stream を作成し、1. で作成した Elasticsearch domain に関連付けます。
3. AWS Lambda の Lambda function を作成し、 lambda_function.py の内容をペーストします。このサンプルコードは Python 2.7 環境にて動作を確認しています。
4. Lambda function を実行する IAM Role が 2. で作成した Kinesis Firehose の Delivery Stream に PutRecord できるように IAM Policy を記述します。
5. Amazon API Gateway において API を作成し、任意の Resource に POST メソッドを作成します。
6. 作成したメソッドに3.で作成した Lambda function を紐付けることで、 CSP を受信し Elasticsearch Service に送信することができます。

## 必要な設定
### ソースコード内の設定
設定が必要なのはソースコード中の以下の箇所のみです。

```python
# origin の設定 (チェックしない場合、任意のドメインからレポートを送り放題になってしまう)
origin_domain = "example.com"
# Kinesis Firehose の Delivery Stream 名
firehose_stream_name = "csp-report"
```

コメントに記載した通りにコードを編集してください。

### API Gateway の設定
API Gateway から Lambda function を起動する際、 Body Mapping Templates の設定が必要です。
- Request Body Passthrough: Never
- Content-Type: application/csp-report
- Generate template: Method Request passthrough の設定で生成された Template を設定

上記のように設定することで動作を確認しています。

## 注意点
- 本サンプルで利用している各 AWS サービスは、利用時に利用料金がかかる可能性があります。利用開始前に必ず各サービスの料金ページをチェックするようにしてください。
