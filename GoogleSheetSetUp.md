# Google Sheet Setup Guide

Follow these steps to set up Google Sheets for your project:

---

## Step 1: Create a Google Sheet
1. Go to [Google Sheets](https://sheets.google.com).
2. Create a new spreadsheet.
3. Name the spreadsheet (e.g., "Fastenal Products").
4. Note the name of the sheet (default is usually "Sheet1").

---

## Step 2: Enable Google Sheets API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Library**.
4. Search for **Google Sheets API** and enable it.
5. Search for **Google Drive API** and enable it (required for accessing Google Sheets).

---

## Step 3: Create Service Account Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials** and select **Service Account**.
3. Fill in the required details and click **Create**.
4. In the **Service Account Permissions** step, click **Continue**.
5. In the **Grant users access to this service account** step, click **Done**.
6. After creating the service account, click on it in the credentials list.
7. Go to the **Keys** tab and click **Add Key > Create New Key**.
8. Select **JSON** and download the key file. Save it securely (e.g., `credentials.json`).

---

## Step 4: Share the Google Sheet with the Service Account
1. Open your Google Sheet.
2. Click **Share** in the top-right corner.
3. In the "Share with people and groups" field, enter the email address of your service account. This email is in the format:  
   `your-service-account-name@your-project-id.iam.gserviceaccount.com`.
4. Set the permission to **Editor** and click **Send**.

---

## Step 5: Update Your Code
1. Place the downloaded `credentials.json` file in your project directory.
2. Update the `credentials_file` parameter in your `GoogleSheetService` initialization to point to the path of the `credentials.json` file.

```python
google_sheet_service = GoogleSheetService(
    credentials_file="path/to/credentials.json",  # Replace with the actual path
    sheet_name="Fastenal Products"               # Replace with your Google Sheet name
)