

getNewmail = {
        "mail": {
            "query":"new email",
            "content": "write job request to company"
        }
}

getResponsemail = {
        "mail": {
            "query":"response email",
            "content": "hi, are you interested in this job?"
        }
}

UTILITIES = [
    {
        'enable': True,
        'utility':'GoogleSearchAPIWrapper',
        'func': 'run',
        'tags': 'search',
        'description': 'search google'
    },
    {
        'enable': True,
        'wrapper':'GmailAPIWrapper',
        'func':'_write_new_mail',
        'tags': 'email, new email, mail',
        'description': 'write new email'
    },
    {
        'enable': True,
        'wrapper':'GmailAPIWrapper',
        'func':'_write_response_mail',
        'tags': 'email, response, response email, respond mail',
        'description': 'write reply email'
    }
    ]
