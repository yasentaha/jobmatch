
<div align="center">

<h1>JomBatch</h1>
<img src="assets/logo.png" alt="logo" width="200" height="auto" />
  
<p>
    From JomBatch to Job-Match! 
</p>

<p>
  <a href="https://gitlab.com/web-project-team-2/job-match-system-api/-/graphs/developer">
    <img src="https://img.shields.io/gitlab/contributors/40324946" alt="contributors" />
  </a>
  <a href="https://gitlab.com/web-project-team-2/job-match-system-api/-/issues">
    <img src="https://img.shields.io/gitlab/issues/open-raw/40324946" alt="open issues" />
  </a>
  <a href="https://gitlab.com/web-project-team-2/job-match-system-api/-/commits/developer">
    <img src="https://img.shields.io/gitlab/last-commit/40324946" alt="last commit" />
  </a>

</p>
</div>

<br/>


# Table of Contents

- [About the Project](#about-the-project)
  * [Technologies](#technologies)

<br/>

## About the Project
Welcome to JomBatch* - From JomBatch to Job-Match!

This project contains a RESTful API that covers the main functionality behind a job-matching software over the web. 

Basically, two types of users can access the public part and register or login - companies and professionals. Based on their role, they have access to different endpoints:
- Companies can post job-ads, search for professionals or their resumes and initiate match requests
- Professionals can post resumes, search for companies or their job ads and initiate match requests
- Both can accept or reject match requests or get instant matches (like tinder).

<br/>

> **The name comes from the bulgarian word **jumbish** - slang for spectacle, show (in a chaotic way).*

<br/>

### Technologies
Language: <a href="https://www.python.org/">Python</a>
<br/>
Framework: <a href="https://www.python.org/">Fastapi</a>
<br/>
<br/>

### Database
Relational Database: <a href="https://mariadb.org/">MariDB</a>
<br/>
RDMS: <a href="https://www.mysql.com/">MySQL</a>
<br/>

#### Database Screenshot:
<div align="center">
<img src="assets/DB_screenshot.png" alt="logo" width="auto" height="auto" />
</div>

### Application Structure
For this project, the use of the multi-tier (n-tier) atchitecture was chosen, where data access, application layer and business logic are separated as follows:
<img src="assets/multitier.png" alt="logo" width="auto" height="400" />
</br>
</br>

## Getting Started
</br>

### Prerequisites

After installing Python on your computer, beware that this project uses pip as package manager:

```
py -m ensurepip --upgrade
```
</br>

**FastAPI**
```
pip install fastapi
```
</br>

**MariaDB**
```
pip install mariadb
```
</br>

**PyJWT** - PyJWT - Log-in info is token-based
```
pip install python-jose[cryptography]
```
</br>

**MailJet** -
```
pip install mailjet
```
</br>

**Regex** - JWT - Log-in info is token-based
```
pip install regex
```
</br>

**Clone the project**
```bash
  git clone https://gitlab.com/web-project-team-2/job-match-system-api.git
```
</br>

### Deployment

To deploy this project run the main file and type:


```py
uvicorn main:app --reload
```

## Usage

TO BE CONTINUED.

### Endpoints / Postman

### Functionality and allocation




## Contact


