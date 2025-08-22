#!/usr/bin/env python3
"""
Test script for documentation sync functionality
Simulates the Dify API for testing purposes
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Add the translate directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from sync_and_translate import DocsSynchronizer

# Mock translation responses
MOCK_TRANSLATIONS = {
    "Chinese": """# 常见问题

欢迎来到 Dify 常见问题部分。在这里您可以找到关于使用 Dify 最常见问题的答案。

## 入门

### 什么是 Dify？

Dify 是一个开源的 AI 应用构建平台。它提供了一套全面的工具和功能，帮助您构建、部署和管理 AI 应用程序，无需大量编程知识。

### 如何开始使用 Dify？

开始使用 Dify：

1. **注册** Dify 账户，访问 [dify.ai](https://dify.ai)
2. **创建您的第一个应用程序** 使用我们直观的界面
3. **配置您的 AI 模型** 通过连接到 OpenAI、Anthropic 或其他提供商
4. **测试和迭代** 您的应用程序
5. **部署** 您的 AI 应用程序到生产环境

### 我可以用 Dify 构建什么类型的应用程序？

您可以使用 Dify 构建各种类型的 AI 应用程序：

- **聊天机器人** 用于客户服务
- **知识库助手** 可以回答有关您文档的问题
- **工作流自动化工具** 智能处理数据
- **内容生成工具** 用于营销和写作
- **AI 代理** 可以执行复杂任务

## 技术问题

### Dify 支持哪些 AI 模型？

Dify 支持广泛的 AI 模型，包括：

- **OpenAI 模型**: GPT-4、GPT-3.5 等
- **Anthropic 模型**: Claude 3 和 Claude 2
- **开源模型**: 通过 Hugging Face、Ollama 等提供商
- **本地模型**: 您可以托管自己的模型

### Dify 如何处理我的数据？

数据安全和隐私是我们的首要任务：

- **您的数据仍然是您的** - 我们不会使用您的私人数据进行训练
- **传输中和静态加密**
- **企业客户的 SOC2 合规性**
- **欧洲用户的 GDPR 合规性**

### 我可以将 Dify 用于商业目的吗？

是的！Dify 提供：

- **开源版本** 带有 Apache 2.0 许可证，用于自托管
- **云版本** 带有托管托管的商业计划
- **企业计划** 具有高级功能和支持

## 故障排除

### 我的 AI 应用程序给出了错误的响应

尝试这些故障排除步骤：

1. **检查您的提示** - 确保它清晰具体
2. **检查您的知识库** - 确保上传了相关文档
3. **调整模型参数** - 尝试不同的温度或 top-k 设置
4. **使用不同的模型测试** - 某些模型更适合特定任务

### 我遇到了响应时间慢的问题

改善响应时间：

1. **检查您的模型配置** - 某些模型比其他模型更快
2. **优化您的知识库** - 删除不必要的文档
3. **使用缓存** - 为常见问题启用响应缓存
4. **考虑升级** 您的计划以获得更好的性能

### 如何获得支持？

您可以通过以下方式获得支持：

- **社区论坛** - 与其他 Dify 用户联系
- **文档** - 全面的指南和教程
- **GitHub 问题** - 用于错误报告和功能请求
- **电子邮件支持** - 适用于付费计划客户
- **企业支持** - 为企业客户提供专门支持

## 计费和计划

### 不同的定价计划有哪些？

Dify 提供几种计划：

- **免费层** - 非常适合入门和小项目
- **专业计划** - 适用于使用需求较高的成长型企业
- **企业计划** - 为大型组织提供定制解决方案

### 如何计算使用量？

使用量通常基于以下因素计算：

- **API 调用** 到 AI 模型
- **存储** 文档和数据
- **活跃用户** 在您的应用程序上
- **自定义功能** 取决于您的计划

有关详细的定价信息，请访问我们的 [定价页面](https://dify.ai/pricing)。

---

需要更多帮助？联系我们的支持团队或查看我们的 [综合文档](../../../guides/)。""",
    
    "Japanese": """# よくある質問

Dify FAQ セクションへようこそ。ここでは、Dify の使用に関してよく寄せられる質問への回答を見つけることができます。

## はじめに

### Dify とは何ですか？

Dify は AI アプリケーションを構築するためのオープンソースプラットフォームです。広範なコーディング知識を必要とせずに、AI アプリケーションの構築、デプロイ、管理を支援する包括的なツールと機能セットを提供します。

### Dify を始めるにはどうすればよいですか？

Dify を開始するには：

1. [dify.ai](https://dify.ai) で Dify アカウントに **サインアップ** してください
2. 直感的なインターフェースを使用して **最初のアプリケーションを作成** してください
3. OpenAI、Anthropic、その他のプロバイダーに接続して **AI モデルを設定** してください
4. アプリケーションを **テストし、反復** してください
5. AI アプリケーションを本番環境に **デプロイ** してください

### Dify でどのようなタイプのアプリケーションを構築できますか？

Dify でさまざまなタイプの AI アプリケーションを構築できます：

- カスタマーサービス用の **チャットボット**
- ドキュメントに関する質問に答えることができる **ナレッジベースアシスタント**
- データを知的に処理する **ワークフロー自動化ツール**
- マーケティングや執筆用の **コンテンツ生成ツール**
- 複雑なタスクを実行できる **AI エージェント**

## 技術的な質問

### Dify はどの AI モデルをサポートしていますか？

Dify は幅広い AI モデルをサポートしています：

- **OpenAI モデル**: GPT-4、GPT-3.5 など
- **Anthropic モデル**: Claude 3 と Claude 2
- **オープンソースモデル**: Hugging Face、Ollama などのプロバイダー経由
- **ローカルモデル**: 独自のモデルをホストできます

### Dify は私のデータをどのように処理しますか？

データセキュリティとプライバシーが最優先事項です：

- **あなたのデータはあなたのもの** - 私たちはあなたのプライベートデータでトレーニングしません
- 転送中および保存時の **暗号化**
- エンタープライズ顧客向けの **SOC2 コンプライアンス**
- ヨーロッパユーザー向けの **GDPR コンプライアンス**

### Dify を商用目的で使用できますか？

はい！Dify は以下を提供しています：

- セルフホスティング用の Apache 2.0 ライセンス付き **オープンソース版**
- マネージドホスティング用の商用プラン付き **クラウド版**
- 高度な機能とサポート付き **エンタープライズプラン**

## トラブルシューティング

### AI アプリケーションが間違った回答をしています

これらのトラブルシューティング手順を試してください：

1. **プロンプトを確認** - 明確で具体的であることを確認してください
2. **ナレッジベースを確認** - 関連するドキュメントがアップロードされていることを確認してください
3. **モデルパラメータを調整** - 異なる温度や top-k 設定を試してください
4. **異なるモデルでテスト** - 一部のモデルは特定のタスクにより適しています

### 応答時間が遅い問題が発生しています

応答時間を改善するには：

1. **モデル設定を確認** - 一部のモデルは他のモデルよりも高速です
2. **ナレッジベースを最適化** - 不要なドキュメントを削除してください
3. **キャッシュを使用** - よくある質問に対してレスポンスキャッシュを有効にしてください
4. **プランのアップグレードを検討** - より良いパフォーマンスのために

### サポートを受けるにはどうすればよいですか？

以下の方法でサポートを受けることができます：

- **コミュニティフォーラム** - 他の Dify ユーザーとつながる
- **ドキュメント** - 包括的なガイドとチュートリアル
- **GitHub の課題** - バグレポートと機能リクエスト用
- **メールサポート** - 有料プラン顧客向け
- **エンタープライズサポート** - エンタープライズ顧客専用サポート

## 請求とプラン

### 異なる価格プランは何ですか？

Dify はいくつかのプランを提供しています：

- **無料ティア** - はじめと小さなプロジェクトに最適
- **プロプラン** - より高い使用ニーズを持つ成長企業向け
- **エンタープライズプラン** - 大規模組織向けのカスタムソリューション

### 使用量はどのように計算されますか？

使用量は通常以下に基づいて計算されます：

- AI モデルへの **API 呼び出し**
- ドキュメントとデータの **ストレージ**
- アプリケーションの **アクティブユーザー**
- プランに応じた **カスタム機能**

詳細な価格情報については、[価格ページ](https://dify.ai/pricing) をご覧ください。

---

さらにヘルプが必要ですか？サポートチームにお問い合わせいただくか、[包括的なドキュメント](../../../guides/) をご確認ください。"""
}

async def mock_translate_text(file_path, dify_api_key, original_language, target_language, termbase_path=None, max_retries=3):
    """Mock translation function that returns predefined translations"""
    print(f"MOCK: Translating {file_path} from {original_language} to {target_language}")
    
    # Simulate processing time
    await asyncio.sleep(0.5)
    
    if target_language == "Chinese":
        return MOCK_TRANSLATIONS["Chinese"]
    elif target_language == "Japanese":
        return MOCK_TRANSLATIONS["Japanese"]
    else:
        return "Mock translation for " + target_language

async def test_sync_workflow():
    """Test the synchronization workflow"""
    print("=== Testing Documentation Sync Workflow ===")
    
    # Create a mock API key
    mock_api_key = "test_api_key_12345"
    
    # Patch the translate_text function
    with patch('sync_and_translate.translate_text', side_effect=mock_translate_text):
        # Initialize synchronizer
        synchronizer = DocsSynchronizer(mock_api_key)
        
        # Test the sync process with git changes
        print("\n1. Testing change detection...")
        changes = synchronizer.get_changed_files("HEAD~1")
        print(f"Detected changes: {changes}")
        
        # Test file operations
        print("\n2. Testing file operations...")
        file_ops = synchronizer.sync_file_operations(changes)
        for op in file_ops:
            print(f"  {op}")
        
        # Test translation (this will actually create files)
        print("\n3. Testing translation process...")
        translations = await synchronizer.translate_new_and_modified_files(changes)
        for trans in translations:
            print(f"  {trans}")
        
        # Test docs.json structure sync
        print("\n4. Testing docs.json structure sync...")
        structure_sync = synchronizer.sync_docs_json_structure()
        for sync in structure_sync:
            print(f"  {sync}")
        
        # Run full sync
        print("\n5. Running full synchronization...")
        results = await synchronizer.run_sync("HEAD~1")
        
        print("\n=== FINAL RESULTS ===")
        for category, logs in results.items():
            if logs:
                print(f"\n{category.upper()}:")
                for log in logs:
                    print(f"  {log}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_sync_workflow())