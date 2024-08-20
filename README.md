# OnePTE Backend Clone for LIILab
OnePTE Backend clone is a project to mimic a subset of backend funtionality of [OnePTE](https://app.onepte.com/) website. To make this project **Django** has been used as Backend Python framework. **Django-Ninja** library has been used to design API.

### Instructions to run the project:
1. Install Python 3.11 or above.
2. Download the *_"OnePTE Backend Clone for LIILab"_* repository and extract the files.
![Download](/instruction_images/download_onepte.png)
3. Open the powershell terminal in the file's directory where `manage.py` file lies and run `python -m venv venv` to create a virtual environment.
![Create venv](/instruction_images/create_venv.png)

4. Activate virtual environment by running `venv/scripts/Activate` command.
![Activate venv](/instruction_images/activate.png)
5. Install the required libraries with the following code `pip install -r requirements.txt` .
![Install Requirements](/instruction_images/install_libraries.png)
6. Run local server with the `python manage.py runserver` command.
![Run Server](/instruction_images/run_server.png)

### Instructions to test API:
* Install **Thunder Client** plugin in __VSCode__ for API testing.
![Thunder Client](/instruction_images/thunder_client.png)
* Import the *_"Thunder Client API Collection.json"_* file into Thunder Client to get API collection.
![Import](/instruction_images/import.png)
![API Collection .json file](/instruction_images/api_collection.png)
* Right Click on each item in the collection and Run request to Test the API.
![Run Request](/instruction_images/run_request.png)

> [!NOTE]
> Assuming that local server is running at `127.0.0.1:8000` 
* There are two api endpoints:
    * `127.0.0.1:8000/oenpte/api` is to get question and submit answer. It takes "type" and "id" query parameter to retrive question and only "type" query parameter to submit answer.\
    For example- `127.0.0.1:8000/oenpte/api?type=sst&id=2` retrieve sst type question with id 2.
    ![API Testing](/instruction_images/api_test_get_question.png)

    * `127.0.0.1:8000/oenpte/api/answer` end point just retrieve a user's answer history. It takes "type" and "username" query parameter.\
    For example- `127.0.0.1:8000/oenpte/api/answer?type=mcq&username=john` retrieve all the MCQ type question's answer that has been submitted by the user with username john.
    ![API Testing](/instruction_images/api_test_get_all_answer.png)

* One can check API documentation and test API by going to the url `127.0.0.1:8000/oenpte/docs` .
![API Documentations](/instruction_images/swagger_docs.png)