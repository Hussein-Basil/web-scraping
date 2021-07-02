import requests, json
from send_email import send_email

api = "https://remoteok.io/api"

keys = ['date', 'company', 'position', 'tags', 'location', 'url']
wanted_tags = {"react"}

def get_jobs():
    response = requests.get(api)
    data = response.json()
    jobs = []

    for job in data:
        job = {k: v for k, v in job.items() if k in keys}
        if job:
            tags = {tag.lower() for tag in job.get('tags')}
            if tags.intersection(wanted_tags):
                jobs.append(job)
    
    return jobs
    
if __name__ == '__main__':
    jobs_ = get_jobs()

    if jobs_:
        message = "Subject: Remote Python Jobs!\n\n"
        message += "Found some cool Python jobs!\n\n"

        for job in jobs_:
            message += f"{json.dumps(job)}\n\n"

        send_email(message)