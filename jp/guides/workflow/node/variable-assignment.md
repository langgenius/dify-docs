# 変数代入

### 定義

変数代入ノードは、書き込み可能な変数に他の変数を代入するために使用されます。現在、サポートされている可書き入れの変数は：

* [会話変数](../key-concept.md##hui-hua-bian-shu)

使用方法：このノードを使用することで、ワークフローの中で変数の値を会話変数に一時的に保存し、後続の会話でその値を参照することができます。

<figure><img src="../../../../img/variable-assigner.png" alt="" width="375"><figcaption></figcaption></figure>

***

### 使用シナリオの例

変数代入ノードを活用することで、会話中の**コンテキスト、ダイアログにアップロードされたファイル（近々配布予定）、ユーザーの好みの情報**などを会話変数に書き込み、保存された情報は後続の会話で参照され、異なる処理フローに誘導したり、返答を行ったりすることができます。

**シナリオ 1** &#x20;

**会話中の記録を自動的に抽出し保存します**、会話変数配列を使用してユーザーの重要な情報を記録します。その後の会話ではこれらの記録を活用し、個別の返信を行います。

例えば：会話が始まると、LLMはユーザーの入力に必要な情報や好み、またはチャット履歴が含まれているかを自動的に判断します。情報が存在する場合、LLMはそれを先に抽出して保存し、コンテキストとして利用して応答します。もし新しい情報を覚える必要がない場合、LLMは以前の関連する記録を用いて個性化な応答を出します。

<figure><img src="../../../../img/conversational-variables-scenario-01.png" alt=""><figcaption></figcaption></figure>

**設定手順：**

1. **会話変数を設定**：まず、会話変数配列 `memories` を設定し、array\[object]型を持たせてユーザーの事実、好み、会話記録を保存します。
2. **記録の判断と抽出**：
   * 条件判断ノードを追加し、LLMを使用してユーザーの入力に新しい情報が含まれているかを判断します。
   * 新しい情報がある場合は上流に進み、LLMノードを使用してこれらの情報を抽出します。
   * 新しい情報がない場合は下流に進み、既存の記憶を直接使用して返答します。
3. **変数の代入と書き込み**：
   * 上流に進んだ後、変数代入ノードを用いて抽出した新しい情報を `memories` 配列に追加(append)します。
   * LLMの出力テキスト文字列を適切な array\[object] 形式に変換するためにエスケープ機能を使用します。
4. **変数の読み取りと利用**：
   * 後続のLLMノードで、`memories` 配列の内容を文字列に変換し、LLMのプロンプトにコンテキストとして挿入します。
   * LLMはこれらの記憶を使用して個別の返信を生成します。

図中のcodeノードのコードは以下の通りです：

1. 文字列をオブジェクトに変換する

```python
import json

def main(arg1: str) -> object:
    try:
        # Parse the input JSON string
        input_data = json.loads(arg1)
        
        # Extract the memory object
        memory = input_data.get("memory", {})
        
        # Construct the return object
        result = {
            "facts": memory.get("facts", []),
            "preferences": memory.get("preferences", []),
            "memories": memory.get("memories", [])
        }
        
        return {
            "mem": result
        }
    except json.JSONDecodeError:
        return {
            "result": "Error: Invalid JSON string"
        }
    except Exception as e:
        return {
            "result": f"Error: {str(e)}"
        }
```

2. オブジェクトを文字列に変換する

```python
import json

def main(arg1: list) -> str:
    try:
        # Assume arg1[0] is the dictionary we need to process
        context = arg1[0] if arg1 else {}
        
        # Construct the memory object
        memory = {"memory": context}
        
        # Convert the object to a JSON string
        json_str = json.dumps(memory, ensure_ascii=False, indent=2)
        
        # Wrap the JSON string in <answer> tags
        result = f"<answer>{json_str}</answer>"
        
        return {
            "result": result
        }
    except Exception as e:
        return {
            "result": f"<answer>Error: {str(e)}</answer>"
        }
```

**シナリオ 2**

**ユーザーの初期の好み情報を記録**し，会話中にユーザーが入力した言語の好みを記憶し、後続の会話でその言語を使用して返信します。

例：ユーザーが会話を始める前に、`language`入力欄に「日本語」と指定した場合、その言語は会話変数に書き込まれ、LLMは後続の返信時に会話変数の情報を参照し、継続的に「日本語」を使用して返信します。

<figure><img src="../../../../img/conversation-var-scenario-1.png" alt=""><figcaption></figcaption></figure>

**設定手順：**

**会話変数の設定**：まず、会話変数 `language` を設定し、会話の開始時にこの変数の値が空かどうかを判断する条件分岐ノードを追加します。

**変数の書き込み/代入**：最初の会話が開始された際、 `language` 変数の値が空であれば、LLMノードを使用してユーザーの言語入力を抽出し、その言語タイプを会話変数 `language` に書き込みます。

**変数の読み取り**：後続の会話ラウンドでは、`language` 変数にユーザーの好みの言語が保存されています。以降の会話では、LLMノードがこの変数を参照し、ユーザーの好みの言語タイプを用いて返信します。

**シナリオ 3**

**Checklistのチェックを補助**し、会話中に会話変数にユーザーの入力項目を記録し、Checklistの内容を更新し、後続の会話で抜け漏れ項目を確認します。

例：会話を始める際、LLMはユーザーにチェックリストに関連するアイテムの入力を求めます。ユーザーがチェックリストの内容を一度述べると、その内容は会話変数に更新され、及び保存されます。LLMは各会話の後に、ユーザーに不足しているアイテムの追加を促します。

<figure><img src="../../../../img/conversation-var-scenario-2-1.png" alt=""><figcaption></figcaption></figure>

**配置流程：**

* **会話変数の設定**：最初に会話変数 `ai_checklist` を設定し、これをLLM内でチェックのコンテクストとして参照します。
* **変数の書き込み/代入**：各会話のラウンドごとに、LLMノード内の `ai_checklist` の値を確認し、ユーザーの入力と比較します。ユーザーが新しい情報を提供した場合、チェックリストを更新し、変数代入ノードを使用して出力内容を `ai_checklist` に書き込みます。
* **変数の読み取り**：`ai_checklist`の値を読み取り、すべてのチェックリストアイテムが完了するまで、各会話のラウンドでユーザーの入力と比較します。

***

### 3 操作方法

**変数代入の使用：**

ノードの右側の `＋` マークをクリックし、「変数代入」 ノードを選択し、「代入られた変数」 と 「設定する変数」 を入力します。

<figure><img src="../../../../img/language-variable-assigner.png" alt="" width="375"><figcaption></figcaption></figure>

**変数の設定：**

代入られた変数：代入された変数を選択し、対象の会話変数を指定します

設定する変数：変換する必要のあるソース変数を選択します

上図の代入ロジック：`Language Recognition/text` を `language` に代入します。&#x20;

**書き込みモード：**

* Overwrite 上書き: ソース変数の内容を対象の会話変数に上書きします
* Append 追加：指定された変数が配列型の場合に使用します
* Clear クリア: 対象の会話変数内の内容をクリアします

