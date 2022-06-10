# モダンなHDLテンプレートリポジトリ

このリポジトリはHDLのモダンなPythonプロジェクト向けテンプレートリポジトリです．

## 構造

```bash
.
├── .editorconfig     # コーディング規則が書かれたファイル
├── .github
│   ├── ISSUE_TEMPLATE.md         # Issueのテンプレート
│   ├── PULL_REQUEST_TEMPLATE.md  # PRのテンプレート
│   └── workflow
│       └── ci.yaml   # Github Actionの設定ファイル
├── .gitignore        # Git追跡しないファイルの設定
├── hdl_template      # 作成するPythonライブラリのルートディレクトリ
│   └── __init__.py   # __init__.pyは必須なので消さないこと
├── pyproject.toml    # パッケージの情報が記載されたファイル
├── README.md         # 本マニュアル
└── test
    └── test_dummy.py # テストコードサンプル

```

## テンプレートを利用したリポジトリの作成方法

[[テンプレートからリポジトリを作成する]](https://help.github.com/ja/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template)を参照してください．

## パッケージマネージャ `Poetry` のインストール
このテンプレートではPythonのパッケージマネージャとして[Poetry](https://python-poetry.org/)を使用しています.  
Poetryがインストールされていない環境では以下のコマンドを実行して事前にインストールする必要があります.  
```bash
$ sudo apt update && sudo apt install python3-venv
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
$ echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.bashrc

# Bash使いの場合
$ echo 'source <(poetry completions bash 2>/dev/null)' >> ~/.bashrc

# Zsh使いの場合 (動作未確認)
$ echo 'source <(poetry completions zsh 2>/dev/null)' >> ~/.zshrc

```

また, 以下のコマンドによりPoetryを最新の状態にアップデートできます.  
```bash
$ poetry self update

```

初期設定では, Poetryは `$HOME/.cache/poetry` 内にvirtualenvを作成します.  
プロジェクトフォルダ内に作成するように変更するには以下のコマンドを叩きます.  
```bash
$ poetry config virtualenvs.in-project true

```

また, そもそもvirtualenvを作らないように設定するには以下のコマンドを叩きます.
```bash
$ poetry config virtualenvs.create false

```

## 初期設定方法
1. `hdl_template/`をあなたの好きなライブラリ名に変えます (e.g. `my_awesome_library/`)
2. `pyproject.toml`を編集します
    - `[tool.poetry.dependencies]` に依存ライブラリを追加します. GitHubに置かれたライブラリも入れられることに注目！！
    - `[tool.poetry.dev-dependencies]` に開発時に必要なライブラリを追加します
    - `[tool.poetry]` 内の情報を変更します
        - 特に`name`などは必ず変更しましょう
3. 試しにインストールしてみましょう  
   `poetry install`  
   依存しているライブラリがインストールされ, `poetry.lock` ファイルが出現します.  
   このファイルにはインストールされたライブラリのバージョン情報が記載されており,
   このファイルが存在する状態で `poetry install` を叩くとlockファイルに記載されているバージョンの
   ライブラリがインストールされます.  
   ちなみに以下のコマンドでもパッケージのインストールが可能です (裏でpoetryが起動します).  
   `pip install .`
4. 試しに呼び出してみましょう  
   `poetry shell`  
   でvirtualenvをactivateして  
   `python -c "import my_awesome_library; print(my_awesome_library.__version__)"`
5. `my_awesome_library/`下にどんどん機能を追加していきましょう
6. 最高のライブラリが完成！

## テストの追加

良いライブラリを作るにはテストコードが必須です．  
`test/test_dummy.py`にPytestライブラリを利用したサンプルコードがおいてありますので，こちらを参考にしてテストを追加しましょう！  
`test/`ディレクトリ化に`test_*.py`というファイルを作り，内部で`def test_hogehoge()`を作成するとPytestで自動的に実行されます．  
テストの実行方法は`pytest`コマンドを呼び出すだけです．
```bash
$ pytest
========================================================= test session starts =========================================================
platform linux -- Python 3.6.4, pytest-3.9.1, py-1.7.0, pluggy-0.8.0 -- /home/t_hayashi/.pyenv/versions/3.6.4/bin/python3.6
cachedir: .pytest_cache
rootdir: /work5/t_hayashi/work/hdl-template, inifile: setup.cfg
plugins: pythonpath-0.7.3, profiling-1.7.0, flake8-1.0.4, cov-2.8.1
collected 4 items

test/test_dummy.py::test_dummy PASSED                                                                                           [ 25%]
test/test_dummy.py::test_pytest_decorator[this-is-test] PASSED                                                                  [ 50%]
test/test_dummy.py::test_pytest_decorator[that-is-test] PASSED                                                                  [ 75%]
test/test_dummy.py::test_pytest_decorator[it-is-test] PASSED                                                                    [100%]

======================================================= slowest test durations ========================================================
0.01s setup    test/test_dummy.py::test_pytest_decorator[this-is-test]

(0.00 durations hidden.  Use -vv to show these durations.)
====================================================== 4 passed in 0.17 seconds =======================================================
```
どんどんテストを追加して，できるだけ早期のバグ発見を目指しましょう！

## CIの設定

`.github/workflow/ci.yaml`にCIの設定があります．  
これを変更することで，githubにpushするたびに自動でLinterやPytestが走りバグの早期発見に繋がります．  
積極的に活用していきましょう！

また, `.github/sample-workflow/*.yaml` にサンプルのCI設定があります.  
参考にしましょう！

## PythonのDocstringについて

PythonのDocstringを整備することは明日の自分へエールを送ることに繋がります．  
積極的に整備していきましょう．  
HDLでは，Google styleのDocstringを推奨しています．  
是非書き方をマスターしましょう！  

参考: [Example Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html#example-google)

## コンテナ化

テンプレートの状態でコンテナイメージのビルド・実行・パブリッシュが行えるようになっています.  

### コマンド集
#### ビルド
```bash
$ make build-image

```

#### 実行
```bash
$ make run-image

```

#### パブリッシュ
```bash
$ make publish-image

```

### カスタマイズ
イメージタグをカスタマイズしたい場合は  
```bash
$ export VERSION=<任意のタグ>
$ make build-image ( or run-image or publish-image )

```
で可能です.  

イメージのレジストリを変えたい場合は `Makefile` の `IMAGE_PREFIX` を編集してください.  
イメージ名はデフォルトではMakefileが置かれているフォルダの名前が使用されますが、 `Makefile` の `IMAGE_NAME` で編集可能です.

### ビルドと公開の自動化
`.github/sample-workflows/image.yaml` を `.github/workflows` にコピーすることで、コンテナイメージのビルドと公開を自動化できます.  
Secretの設定方法は[こちら](https://www.notion.so/humandatawarelab/GitHub-CI-Secret-12c9dbfd87fc451e876422869947fff3).
