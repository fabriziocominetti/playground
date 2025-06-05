# Email Slicer Program

# get the user's email address
email = input("What's your email address?: ").strip()

# slice out the user's name
user_name = email[:email.index("@")]
# slice out the domain
domain = email[email.index("@")+1:]

# format message
res = f"Your username is '{user_name}' and your domain is '{domain}'"

print(res)