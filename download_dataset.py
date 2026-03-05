import os
import requests

urls = [
"https://miro.medium.com/v2/resize:fit:1400/1*5gJzumm0TnJ6vUMlzUxrKw.png",
"https://miro.medium.com/v2/resize:fit:1400/1*3PqZK0s8AjtKoa6HgMHqYQ.png",
"https://docs.aws.amazon.com/images/architecture-diagrams/latest/microservices-on-aws/images/microservices-on-aws.png",
"https://docs.aws.amazon.com/images/wellarchitected/latest/serverless-applications-lens/images/serverless-reference-architecture.png",
"https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/media/aks/aks-architecture.png",
"https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/media/app-service-web-app/app-service-web-app.png",
"https://miro.medium.com/v2/resize:fit:1400/1*7XKp2qxGn8pYtBXexdFvkw.png",
"https://miro.medium.com/v2/resize:fit:1400/1*H1-8ZndKyVKoU9pYNCXS6A.png",
"https://miro.medium.com/v2/resize:fit:1400/1*Y9qsK0R12xlfL6Nq35p3xg.png",
"https://miro.medium.com/v2/resize:fit:1400/1*2nE4yoynZMhUlCT3VkOITg.png"
]

os.makedirs("data/raw", exist_ok=True)

for i, url in enumerate(urls):
    try:
        r = requests.get(url)
        with open(f"data/raw/arch_{i}.png", "wb") as f:
            f.write(r.content)
        print("baixado", url)
    except:
        print("erro", url)