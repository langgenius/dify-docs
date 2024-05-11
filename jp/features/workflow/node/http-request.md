# HTTP Request

HTTP Request node lets you craft and dispatch HTTP requests to specified endpoints, enabling a wide range of integrations and data exchanges with external services. The node supports all common HTTP request methods, and lets you fully customize over the URL, headers, query parameters, body content, and authorization details of the request.

<figure><img src="../../../.gitbook/assets/06f7c6ba-fbe0-4aeb-b7d4-fa1df0b07a5e.png" alt="" width="375"><figcaption></figcaption></figure>

A really handy feature with HTTP request is the ability to dynamically construct the request by inserting variables in different fields. For instance, in a customer support scenario, variables such as username or customer ID can be used to personalize automated responses sent via a POST request, or retrieve individual-specific information related to the customer.The HTTP request returns `body`, `status_code`, `headers`, and `files` as outputs. If the response includes files of [MIME](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics\_of\_HTTP/MIME\_types/Common\_types) types (currently limited to images), the node automatically saves these as `files` for downstream use.
