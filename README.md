# iDealAIHelper

#### Description
iDealAI Assistant is a web-based system that encapsulates various AI tool interfaces. It has integrated the ChatGPT API interface (support for other AI platforms’ interfaces is under development).

ChatGPT supports a shared mode using an openai account and also supports a personal independent billing method using one’s own API_key. It is suitable not only for individuals and others to share ChatGPT accounts, but also for domestic enterprises to independently deploy and provide to employees for use, solving the problem of inability to access openai’s interfaces in China.


There are two ways to use the system with ChatGPT:

1 Shared mode
It supports sharing one openai account for everyone to use together. However, each person has an independent system login account, and the sessions can be stored separately.

2 Independent mode
It supports individuals using their own API_key to use the system, and provides corresponding account management, history session storage, and export functions.

This project thanks the work of experts such as acheong08. The shared mode basically continues his work, and we focus on expanding the session processing and front-end development docking work under the independent mode.

In terms of deployment, we try to simplify it as much as possible so that users can quickly deploy and plug-and-play.

#### Software Architecture
The system is divided into two parts: the front-end and the back-end interface.

1 The front-end uses technologies such as Vue3, TypeScript, Vite, and Naive-UI.

2 The back-end uses the Python programming language and the FastAPI framework. To simplify deployment, the database uses SQLite storage, which can also be extended to MySQL.

Both parts can be quickly deployed in containers.

#### Installation

##### Deploy using Docker.

1. Make sure that docker and docker-compose software are installed on the server.

2. download project：
`git clone https://gitee.com/ncepu-bj/iDeal-AI-Helper.git` ，
 Enter the folder named "iDeal-AI-Helper"：
 `cd iDeal-AI-Helper`

3. Modify the system configuration file：`deploy/config.conf`.If you enable the shared mode, you must configure the chatgpt_access_token parameter.
note：how to get chatgpt_access_token parameter ：login [chat.openai.com]()，open [https://chat.openai.com/api/auth/session]()，you can get accessToken value，then copy it into your configuration file；

4. Run the command docker-compose up -d in the project root directory. If an error occurs, please check the docker-compose version. If the version is too low, an upgrade is required. The container port is defined in the docker-compose.yaml file and is mapped to port 8080 by default. It can be modified according to requirements.

5. Access http://[your server ip]:8080 to see the login page (enter the default account/password: admin/admin). If you can log in successfully, the deployment is complete.

##### Manual Deployment

##### Frontend page packing and compiling:

1. Go to the frontend folder “frontend”; If there is already a compiled static page folder “dist”, go directly to the “Backend Deployment” section. Otherwise, proceed to the next step to package and compile the frontend page.
2. Run npm install and npm run build to package and compile the frontend static page. The compiled files will be generated in the frontend/dist folder.

##### Backend Deployment:

1. Create a Python virtual environment (recommended version V3.10) and activate it;
2. Enter the backend folder, install system dependencies by running: pip install -r requirements.txt;
3. In the backend folder, run: uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips '*' --log-config config/logging_config.yaml;
4. Use the frontend/dist/ directory as the publishing directory for the web. You can configure the frontend and backend services using nginx, as shown in the following configuration example：

```
server {
	listen 80;
	server_name [your server name];

    # ui
    location / {
        root [your project abspath]/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    # api
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
5. After starting the Nginx web server, visit http://[your server ip] to see the login page (enter default username/password: admin/admin). If you can log in successfully, then the deployment is complete.


#### System features

Rich frontend interactive operations:
1. A beautiful and concise web interface, using naive-ui
2. Adaptable to a dark mode
3. Support for one-click copying of response content or code content
Support for displaying images/tables/mathematical formulas/code syntax highlighting in responses
4. One-click export of conversations as Markdown files
5. Dynamically display response content
6. Support for stopping conversation generation
7. Multi-user shared management

Share a ChatGPT account, support for creating and managing multiple user accounts:
1. Different users’ ChatGPT conversations are separated from each other and do not affect each other
2. ultiple users requesting at the same time will be queued for processing

Perfect management functions:
1. Administrators can set the maximum number of conversations for users, conversation frequency limits, etc.
2. rovide real-time updates of service usage status to avoid peak usage
Modify user conversation restrictions
3. Manage conversations/view member conversation records/assign.
4. conversations to specific users
5. Real-time view of logs
6. Record request and conversation statistics


#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request


####  Instructions for use

After deployment, access the system via the IP address and port. The system already comes with 2 default users.

First, log in using the administrator account (admin/admin) and then create new user accounts.

For detailed instructions, please refer to the help documentation.

#### How to Contribution:

1. Fork this repository
2. Create a new branch called Feat_xxx
3. Submit your code changes
4. Create a new Pull Request


#### Donation and Support
If you find this project helpful for your work, you can donate and support us by scanning the QR code below. Your encouragement will motivate us to make it even better!

<img src=".github/images/donate.png" alt="donate" width="200" height="200" />