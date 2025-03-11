## Agentic App Backend

Example of App with Agentic AI included.

### Usage

```bash
curl -X POST "http://localhost:8080/ask"      -H "Content-Type: application/json"      -d '{"query": "What is KServe"}'

{"response":"What is KServe\n<tool_call>\nPage: Kubeflow\nSummary: Kubeflow is an open-source platform for machine learning and MLOps on Kubernetes introduced by Google. The different stages in a typical machine learning lifecycle are represented with different software components in Kubeflow, including model development (Kubeflow Notebooks), model training (Kubeflow Pipelines, Kubeflow Training Operator), model serving (KServe), and automated machine learning (Katib).\nEach component of Kubeflow can be deployed separately, and it is not a requirement to deploy every component.\n\n\nKServe is a component of Kubeflow, an open-source platform for machine learning and MLOps on Kubernetes. It is specifically used for model serving. KServe allows you to deploy trained machine learning models as scalable, secure, and high-performance RESTful APIs. It supports multiple runtimes, including TensorFlow Serving, PyTorch Serving, and ONNX Runtime, making it flexible for various machine learning frameworks."}
```