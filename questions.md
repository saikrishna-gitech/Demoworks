DevOps Interview Questions and Answers
Ansible

Q: What is the difference between roles and playbooks in Ansible?
A: Playbooks define tasks in YAML, while Roles organize tasks, variables, templates, handlers, and files into reusable modules. Roles are used for modularity and reusability in large projects.

Q: How do you handle sensitive data like passwords or API keys in Ansible?
A: Use Ansible Vault to encrypt secrets, or integrate with secret managers (HashiCorp Vault, AWS Secrets Manager). Avoid storing plain text credentials in playbooks.

Q: If a playbook fails on the 4th task, how can you debug and rerun only that host/task?
A: Use `ansible-playbook play.yml --start-at-task "Task Name"` or limit to a specific host with `--limit`. For debugging, run with `-vvv`.
Shell Scripting

Q: Write a script to check disk usage and alert if above 80%.

A: #!/bin/bash
THRESHOLD=80
USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $USAGE -gt $THRESHOLD ]; then
  echo "Disk usage above ${THRESHOLD}%: ${USAGE}%"
fi

Q: How do you debug a shell script?
A: Use `set -x` to trace commands, `echo` statements to print variable values, and check exit codes with `$?`.

Q: What is the difference between $* and $@ in shell scripting?
A: $* treats all arguments as a single string, $@ treats them as separate arguments (preferred for loops).
Jenkins & CI/CD

Q: How do you parameterize a Jenkins pipeline for different environments?
A: Use `parameters {}` in Jenkinsfile.
Example:
parameters {
    choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: 'Select Environment')
}
Then use `if (params.ENV == 'prod') { ... }`.
 
Q: If a Jenkins job is failing intermittently, how would you troubleshoot?
A: Check Jenkins logs and agent connectivity, ensure resources (CPU/memory) are sufficient, review flaky tests or unstable dependencies. Add retry logic in pipeline (`retry(3) { ... }`).

Q: What is the difference between a declarative pipeline and a scripted pipeline?
A: Declarative: structured, easier to read/maintain.
Scripted: flexible (Groovy-based), but complex.
Prefer Declarative for CI/CD, Scripted for advanced custom logic.
Python

Q: Write a Python script to read a log file and print only error lines.
A: with open("app.log") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())

Q: How do you handle exceptions in Python automation scripts?
A: try:
    risky_function()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

Q: Why use virtual environments in Python for DevOps automation?
A: They isolate dependencies, prevent conflicts between projects, and make automation scripts reproducible across environments.
Bitbucket / Git

Q: What branching strategy would you use for CI/CD?
A: Use Gitflow or feature-branch workflow:
- Feature branches → PR → develop.
- Release/hotfix branches as needed.
- Master/main only for production-ready code.

Q: What is the difference between rebase and merge? Which one do you prefer?
A: Merge keeps history with a merge commit.
Rebase rewrites commits onto another branch for a clean history.
Rebase for local cleanup, Merge for team collaboration.

Q: How do you resolve merge conflicts?
A: Run `git status` to identify conflicts, edit conflicting files manually, mark resolved with `git add`, then commit or continue the rebase.
Sample Ansible Script

Q: Sample Playbook to install Apache and configure index.html
A: ---
- name: Install and configure Apache web server
  hosts: webservers
  become: yes

  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: present
      when: ansible_os_family == "Debian"

    - name: Start and enable Apache service
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Create custom index.html
      copy:
        dest: /var/www/html/index.html
        content: |
          <html>
          <h1>Welcome to Ansible Webserver</h1>
          </html>
