# podcast_app

Amazon Transcribe APIを使ってmp3ファイルからWordCloudをCUIだけで作成するコード郡です。

処理の流れは以下。

1. mp3ファイルをS3にアップロードする
2. S3のファイルを指定してAmazon Transcribeで文字起こしする
3. 文字起こし結果からWordCloudのpngを生成する



## 1. mp3ファイルをS3にアップロードする

処理: 文字起こししたいmp3ファイルをAmazon S3にアップロードする

```python
python upload_file_to_s3.py /path/to/AudioName.mp3
```

- Input file（引数にとるファイル）: ローカルにあるAudioName.mp3のパス

`bucket_name` に既存のbucket名を指名する

実行すると、S3bucket上にinputしたmp3ファイルがアップロードされる



## 2. S3のファイルを指定してAmazon Transcribeで文字起こしする

処理: S3にアップしたmp3ファイルに対してAmazon Transcribeを実行し文字起こしを行う

```python
python transcribe_aws.py AudioName.mp3
```

- Input file（引数にとるファイル）: AudioName.mp3（S3上にアップロードされたファイル名）

- output file: AudioName.pickle

スクリプトを実行した階層に`transcribed_file`というフォルダを作り、そこにAudioName.pickle ファイルを作成する。pickleファイルの中身は文字起こしされた日本語。



## 3. 文字起こし結果からWordCloudのpngを生成する

処理: 文字起こしされた日本語からWordCloudを作成する

```python
python make_wordcloud.py AudioName.pickle
```

- Input file（引数にとるファイル）: AudioName.pickle

- output file: AuioName.png

スクリプトを実行した階層に`wordcloud_figs`というフォルダを作り、そこにAudioName.png ファイルを作成する。wordcloud化する対象単語のパラメータとして`stop_words`と`min_cnt`がある

