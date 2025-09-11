

## **Ansible**

**Q1. What is the difference between roles and playbooks in Ansible?**
👉 *Playbooks* define tasks in YAML, while *Roles* organize tasks, variables, templates, handlers, and files into reusable modules. Roles are used for modularity and reusability in large projects.

**Q2. How do you handle sensitive data like passwords or API keys in Ansible?**
👉 Use **Ansible Vault** to encrypt secrets, or integrate with secret managers (HashiCorp Vault, AWS Secrets Manager). Avoid storing plain text credentials in playbooks.

**Q3. If a playbook fails on the 4th task, how can you debug and rerun only that host/task?**
👉 Use `ansible-playbook play.yml --start-at-task "Task Name"` or limit to a specific host with `--limit`. For debugging, run with `-vvv`.

Perfect 👍 Since you’re focusing on **Ansible automation**, here are some **interview-ready questions (with answers)** that go beyond the basics and test real hands-on expertise.

---

### **1. Basics of Automation**

**Q1. How does Ansible achieve automation without agents?**
👉 Ansible uses **SSH (for Linux/Unix)** and **WinRM (for Windows)** to communicate with nodes, so no agent is required.

**Q2. How do you make sure your playbooks are idempotent?**
👉 By using Ansible modules instead of raw commands. Modules ensure the state (e.g., `state: present` for packages) is applied only if necessary.

---

### **2. Playbooks & Roles**

**Q3. What is the difference between a playbook and a role in Ansible automation?**
👉 A **playbook** defines tasks for specific hosts, while a **role** is a reusable structure that organizes tasks, variables, templates, and handlers for automation projects.

**Q4. How do you reuse playbooks across projects?**
👉 By converting them into **roles** and storing in a **Galaxy-style directory structure** (roles/tasks, roles/vars, roles/templates).

---

### **3. Variables & Templates**

**Q5. What are the different variable scopes in Ansible?**
👉

* **Playbook variables**
* **Inventory variables (group\_vars, host\_vars)**
* **Role defaults and vars**
* **Extra vars (-e option)** (highest precedence)

**Q6. How would you use Jinja2 templates in automation?**
👉 Use the `template` module to dynamically generate config files. Example:

```yaml
- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
```

### **4. Error Handling & Debugging**

**Q7. How do you handle errors in automation tasks?**
👉

* Use `ignore_errors: yes` for non-critical tasks.
* Use `failed_when` and `changed_when` for custom conditions.
* Use `block/rescue/always` for try-catch style error handling.

**Q8. How do you debug an Ansible playbook?**
👉 Use `-vvv` for verbose logs, `ansible-playbook --check` for dry runs, and `debug` module for printing variable values.

---

### **5. Advanced Automation**

**Q9. How can you make an Ansible playbook dynamic for multiple environments (dev/test/prod)?**
👉

* Use **inventory groups (group\_vars/host\_vars)**.
* Use **`when` conditions** to apply tasks based on environment.
* Pass **extra vars** at runtime (`-e env=prod`).

**Q10. How do you integrate Ansible with CI/CD pipelines?**
👉 By running playbooks inside Jenkins/GitLab CI/CD jobs, typically using:

* Ansible plugin in Jenkins.
* Running `ansible-playbook` as a build/deploy step.
* Storing playbooks in Git and triggering via webhooks.

---

### **6. Collections & Galaxy**

**Q11. What are Ansible Collections?**
👉 Collections are a distribution format for playbooks, roles, plugins, and modules. They help reuse automation content easily (via **Ansible Galaxy** or private repos).

**Q12. How do you install and use a collection?**
👉

```bash
ansible-galaxy collection install community.general
```

Then use it in playbooks:

```yaml
- name: Use community general collection
  community.general.ping:
```

---

### **7. Real-World Automation Scenarios**

**Q13. How would you automate patching 500 Linux servers using Ansible?**
👉

1. Create an inventory of servers.
2. Use `yum`/`apt` modules in a playbook.
3. Run playbook with parallelism (`-f 50`) and serial strategy to control load.
4. Test compliance using `ansible.builtin.command: uname -r`.

**Q14. How do you automate rolling deployments with Ansible?**
👉 Use **`serial`** in playbooks to update a subset of servers at a time (e.g., `serial: 10`). Combine with **handlers** to restart services only when needed.

---

## **Shell Scripting**

**Q1. Write a script to check disk usage and alert if above 80%.**
👉

```bash
#!/bin/bash
THRESHOLD=80
USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $USAGE -gt $THRESHOLD ]; then
  echo "Disk usage above ${THRESHOLD}%: ${USAGE}%"
fi
```

**Q2. How do you debug a shell script?**
👉 Use `set -x` to trace commands, `echo` statements to print variable values, and check exit codes with `$?`.

**Q3. What is the difference between `$*` and `$@` in shell scripting?**
👉 `$*` treats all arguments as a single string, `$@` treats them as separate arguments (preferred for loops).

---

## **Jenkins & CI/CD**

**Q1. How do you parameterize a Jenkins pipeline for different environments?**
👉 Use `parameters {}` in Jenkinsfile. Example:

```groovy
parameters {
    choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: 'Select Environment')
}
```

Then use `if (params.ENV == 'prod') { ... }`.

**Q2. If a Jenkins job is failing intermittently, how would you troubleshoot?**
👉 Check Jenkins logs and agent connectivity, ensure resources (CPU/memory) are sufficient, review flaky tests or unstable dependencies. Add retry logic in pipeline (`retry(3) { ... }`).

**Q3. What is the difference between a declarative pipeline and a scripted pipeline?**
👉 Declarative: structured, easier to read/maintain.
Scripted: flexible (Groovy-based), but complex.
👉 Prefer Declarative for CI/CD, Scripted for advanced custom logic.

---

## **Python**

**Q1. Write a Python script to read a log file and print only error lines.**
👉

```python
with open("app.log") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())
```

**Q2. How do you handle exceptions in Python automation scripts?**
👉 Use `try/except`. Example:

```python
try:
    risky_function()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

**Q3. Why use virtual environments in Python for DevOps automation?**
👉 They isolate dependencies, prevent conflicts between projects, and make automation scripts reproducible across environments.

---

## **Bitbucket / Git**

**Q1. What branching strategy would you use for CI/CD?**
👉 Use Gitflow or feature-branch workflow:

* Feature branches → PR → develop.
* Release/hotfix branches as needed.
* Master/main only for production-ready code.

**Q2. What is the difference between rebase and merge? Which one do you prefer?**
👉 Merge keeps history with a merge commit.
👉 Rebase rewrites commits onto another branch for a clean history.
👉 Rebase for local cleanup, Merge for team collaboration.

**Q3. How do you resolve merge conflicts?**
👉 Run `git status` to identify conflicts, edit conflicting files manually, mark resolved with `git add`, then commit or continue the rebase.

---

## 📌 Sample Ansible Playbook: Install Apache and Start Service

```yaml
---
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
```

---

### 🔎 What this playbook does:

1. Installs **Apache2** (for Debian/Ubuntu).
2. Ensures the **Apache service is running** and enabled at boot.
3. Creates a simple **index.html** page.

---

Here’s a simple Ansible playbook that sets up an Nginx server (I think you meant “inginix” → nginx) on a target Linux machine:

---
- name: Setup sample Nginx server
  hosts: webservers
  become: yes
  tasks:

    - name: Install Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Install Nginx (RHEL/CentOS)
      yum:
        name: nginx
        state: present
      when: ansible_os_family == "RedHat"

    - name: Start and enable Nginx service
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Deploy sample index.html page
      copy:
        dest: /var/www/html/index.html
        content: |
          <html>
          <head><title>Welcome to Sample Nginx Server</title></head>
          <body>
          <h1>Hello from Ansible provisioned Nginx server!</h1>
          </body>
          </html>

    - name: Open HTTP port (80) on firewalld (only for RedHat/CentOS)
      firewalld:
        service: http
        permanent: yes
        state: enabled
        immediate: yes
      when: ansible_os_family == "RedHat"

Steps:

1. Define your inventory file (hosts.ini) like this:

[webservers]
server1 ansible_host=192.168.1.10 ansible_user=ubuntu


2. Run the playbook:

ansible-playbook -i hosts.ini nginx_setup.yml


3. After running, open the server’s IP in your browser → you’ll see the sample HTML page.





