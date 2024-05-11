## 貢献する

あなたがDifyに貢献しようとしているのは素晴らしいことです。私たちはあなたの活動を楽しみにしています。人的資源と資金が限られているスタートアップとして、私たちはLLMアプリケーションの構築と管理に最も直感的なワークフローを設計するという壮大な目標を持っています。コミュニティからの支援は本当に重要です。

私たちは現状を考慮して素早く製品を出荷する必要がありますが、同時に、貢献者の皆さんができるだけスムーズに参加できるようにこのガイドを用意しました。

このガイドはDify自体と同様に、改善し続けております。プロジェクトの現状より遅れることがあるかもしれませんが、改善のためのフィードバックを歓迎します。

ライセンスについては、当社の短い[ライセンスと貢献者契約](./license)をご確認ください。コミュニティでは[行動規範](https://github.com/langgenius/.github/blob/main/CODE_OF_CONDUCT.md)に従います。

## 参加する前に

[探す](https://github.com/langgenius/dify/issues?q=is:issue+is:closed)既存の課題を探すか、新しい課題を[作る](https://github.com/langgenius/dify/issues/new/choose)。課題は次の2つのタイプに分類されます。

### 機能リクエスト：

* 新しい機能リクエストを開く場合、提案された機能が何を達成するかを説明し、できるだけ多くのコンテキストを含めてください。[@perzeusss](https://github.com/perzeuss)が作成した[機能リクエストアシスタント](https://udify.app/chat/MK2kVSnw1gakVwMX)を試してみてください。

* 既存の問題を選ぶ場合は、その下にコメントを残してください。

関連する分野で作業しているチームメンバーが取り組みます。すべてが順調であれば、コーディングを開始するための許可が出されます。私たちが変更を提案する可能性があるため、その許可が出るまで作業を開始しないようお願いします。

提案された機能がどの分野に属するかによって、異なるチームメンバーと話すことになるかもしれません。現在、各チームメンバーが取り組んでいる分野は以下の通りです：

  | Member                                                       | Scope                                                |
  | ------------------------------------------------------------ | ---------------------------------------------------- |
  | [@yeuoly](https://github.com/Yeuoly)                         | Architecting Agents                                  |
  | [@jyong](https://github.com/JohnJyong)                       | RAG pipeline design                                  |
  | [@GarfieldDai](https://github.com/GarfieldDai)               | Building workflow orchestrations                     |
  | [@iamjoel](https://github.com/iamjoel) & [@zxhlyh](https://github.com/zxhlyh) | Making our frontend a breeze to use                  |
  | [@guchenhe](https://github.com/guchenhe) & [@crazywoola](https://github.com/crazywoola) | Developer experience, points of contact for anything |
  | [@takatost](https://github.com/takatost)                     | Overall product direction and architecture           |

  優先順位の付け方は次の通りです：

| Feature Type                                                 | Priority        |
| ------------------------------------------------------------ | --------------- |
| High-Priority Features as being labeled by a team member     | High Priority   |
| Popular feature requests from our [community feedback board](https://github.com/langgenius/dify/discussions/categories/ideas) | Medium Priority |
| Non-core features and minor enhancements                     | Low Priority    |
| Valuable but not immediate                                   | Future-Feature  |

### その他（例：バグレポート、パフォーマンス最適化、タイプミスの修正）：
* コーディングを始めます。

  How we prioritize:

  | Issue Type                                                   | Priority        |
  | ------------------------------------------------------------ | --------------- |
  | Bugs in core functions (cannot login, applications not working, security loopholes) | Critical        |
  | Non-critical bugs, performance boosts                        | Medium Priority |
  | Minor fixes (typos, confusing but working UI)                | Low Priority    |


## インストール

開発のためのDifyのセットアップ手順は以下の通りです：

### 1. このリポジトリをフォークする

### 2. リポジトリをクローンする

ターミナルからフォークしたリポジトリをクローンします：

```
git clone git@github.com:<github_username>/dify.git
```

### 3. 依存関係の確認

Difyを構築するためには以下の依存関係が必要です。システムにインストールされていることを確認してください：

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js v18.x (LTS)](http://nodejs.org)
- [npm](https://www.npmjs.com/) version 8.x.x or [Yarn](https://yarnpkg.com/)
- [Python](https://www.python.org/) version 3.10.x


### 4. インストール

Difyはバックエンドとフロントエンドから構成されています。`cd api/`でバックエンドディレクトリに移動し、[バックエンドのREADME](api/README.md)に従ってインストールしてください。別のターミナルでフロントエンドディレクトリに移動するには`cd web/`を使用し、[フロントエンドのREADME](web/README.md)に従ってインストールしてください。

インストールに関する一般的な問題とトラブルシューティングの手順は、[インストールFAQ](https://docs.dify.ai/getting-started/faq/install-faq)をチェックしてください。

### 5. ブラウザでDifyを訪問する

セットアップを検証するために、ブラウザで[http://localhost:3000](http://localhost:3000)（（デフォルト、または自分で設定したURLとポート）にアクセスします。これで、Difyが動作しているのが確認できます。

## 開発

モデルプロバイダーを追加する場合、この[ガイド](https://github.com/langgenius/dify/blob/main/api/core/model_runtime/README.md)を参考してください。

あなたの貢献がスムーズにできるために、Difyのバックエンドとフロントエンドの概要を簡潔に注釈付きで説明します：

### バックエンド

DifyのバックエンドはPythonで書かれ、[Flask](https://flask.palletsprojects.com/en/3.0.x/)を使用しております。ORMは[SQLAlchemy](https://www.sqlalchemy.org/)を使用し、[Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)をタスクキューとして使用しております。認証ロジックはFlask-loginを介して処理されます。

```
[api/]
├── constants             // Constant settings used throughout code base.
├── controllers           // API route definitions and request handling logic.           
├── core                  // Core application orchestration, model integrations, and tools.
├── docker                // Docker & containerization related configurations.
├── events                // Event handling and processing
├── extensions            // Extensions with 3rd party frameworks/platforms.
├── fields                // field definitions for serialization/marshalling.
├── libs                  // Reusable libraries and helpers.
├── migrations            // Scripts for database migration.
├── models                // Database models & schema definitions.
├── services              // Specifies business logic.
├── storage               // Private key storage.      
├── tasks                 // Handling of async tasks and background jobs.
└── tests
```

### フロントエンド

このWebサイトは[Next.js](https://nextjs.org/)のボイラープレートでTypescriptを用いて構築され、スタイリングには[Tailwind CSS](https://tailwindcss.com/)が使用されています。国際化には[React-i18next](https://react.i18next.com/)を利用しています。

```
[web/]
├── app                   // layouts, pages, and components
│   ├── (commonLayout)    // common layout used throughout the app
│   ├── (shareLayout)     // layouts specifically shared across token-specific sessions 
│   ├── activate          // activate page
│   ├── components        // shared by pages and layouts
│   ├── install           // install page
│   ├── signin            // signin page
│   └── styles            // globally shared styles
├── assets                // Static assets
├── bin                   // scripts ran at build step
├── config                // adjustable settings and options 
├── context               // shared contexts used by different portions of the app
├── dictionaries          // Language-specific translate files 
├── docker                // container configurations
├── hooks                 // Reusable hooks
├── i18n                  // Internationalization configuration
├── models                // describes data models & shapes of API responses
├── public                // meta assets like favicon
├── service               // specifies shapes of API actions
├── test                  
├── types                 // descriptions of function params and return values
└── utils                 // Shared utility functions
```

## あなたのPRを作成

プルリクエスト（PR）を当社のリポジトリに送信しましょう。コアな機能の場合は、最初にテストのために`deploy/dev`ブランチにマージされ、その後`main`ブランチにマージします。マージ競合などの問題が発生した場合やプルリクエストの作り方がわからない場合は、[GitHubのプルリクエストチュートリアル](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)を確認してください。

それだけ！あなたのPRがマージされると、[README](https://github.com/langgenius/dify/blob/main/README.md) に貢献者として掲載いたします。

## ヘルプ

開発中に困ったり、疑問がある場合は、関連するGitHubイシューを通じて問い合わせるか、[Discord](https://discord.gg/AhzKf7dNgk)でチャットをしてください。