# Question Classifier

Question Classifier node defines the categorization conditions for user queries, enabling the LLM to dictate the progression of the dialogue based on these categorizations. As illustrated in a typical customer service robot scenario, the question classifier can serve as a preliminary step to knowledge base retrieval, identifying user intent. Classifying user intent before retrieval can significantly enhance the recall efficiency of the knowledge base.

<figure><img src="../../../.gitbook/assets/image (54).png" alt=""><figcaption></figcaption></figure>

Configuring the Question Classifier Node involves three main components:

1. **Selecting the Input Variable**
2. **Configuring the Inference Model**
3. **Writing the Classification Method**

**Selecting the Input Variable** In conversational customer scenarios, you can use the user input variable from the "Start Node" (sys.query) as the input for the question classifier. In automated/batch processing scenarios, customer feedback or email content can be utilized as input variables.

**Configuring the Inference Model** The question classifier relies on the natural language processing capabilities of the LLM to categorize text. You will need to configure an inference model for the classifier. Before configuring this model, you might need to complete the model setup in "System Settings - Model Provider". The specific configuration method can be found in the [model configuration instructions](https://docs.dify.ai/tutorials/model-configuration#model-integration-settings). After selecting a suitable model, you can configure its parameters.

**Writing Classification Conditions** You can manually add multiple classifications by composing keywords or descriptive sentences that fit each classification. Based on the descriptions of these conditions, the question classifier can route the dialogue to the appropriate process path according to the semantics of the user's input.
