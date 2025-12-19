# Frontend Docusaurus Application Deployment Guide

This document outlines the deployment steps for the Docusaurus frontend application that integrates the RAG Chatbot.

## 1. Prerequisites

-   Node.js (LTS version recommended) and npm/yarn installed.
-   Access to a web hosting service (e.g., Netlify, Vercel, GitHub Pages, AWS S3/CloudFront).
-   The backend FastAPI service must be deployed and accessible.

## 2. Environment Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd physical-AI-and-humanoid-robotics/frontend # Or directly to root if Docusaurus is at root
    ```

2.  **Install dependencies**:
    ```bash
    npm install # or yarn install
    ```

3.  **Configure Environment Variables**:
    The Docusaurus frontend will need to know the URL of the deployed backend API. This is typically configured via environment variables that start with `REACT_APP_` or similar prefixes, which Docusaurus (being a React app) picks up.

    Set the `REACT_APP_API_BASE_URL` variable in your deployment environment:
    ```bash
    REACT_APP_API_BASE_URL="https://your-deployed-backend.com"
    ```
    During local development, you can create a `.env` file in the Docusaurus root directory (or where `package.json` resides) with this variable.

## 3. Building the Application

To build the static Docusaurus site for deployment:

```bash
npm run build # or yarn build
```
This will generate static HTML, CSS, and JavaScript files in the `build/` directory (or `docusaurus-build/` depending on configuration).

## 4. Deployment to a Static Hosting Service

The `build/` directory can be deployed to any static site hosting service.

### Example: Deploying to Netlify

1.  **Connect to your Git repository** in Netlify.
2.  **Configure build settings**:
    -   **Build command**: `npm run build`
    -   **Publish directory**: `build/`
3.  **Set environment variables**: In Netlify UI, add `REACT_APP_API_BASE_URL` with the URL of your deployed backend.

### Example: Deploying to GitHub Pages

You can configure GitHub Actions to deploy your Docusaurus site to GitHub Pages automatically. Refer to the Docusaurus documentation for specific GitHub Pages deployment instructions. Typically, this involves:
1.  Adding a deploy script (e.g., `gh-pages` package).
2.  Configuring a GitHub Actions workflow (e.g., `.github/workflows/deploy.yml`) to build and push the `build/` directory to the `gh-pages` branch.

## 5. Integration with the Chatbot Backend

Ensure the `REACT_APP_API_BASE_URL` environment variable is correctly set in your frontend deployment to point to the live URL of your FastAPI backend service.

## 6. Post-Deployment

-   **Testing**: Verify the chatbot UI loads, sends messages to the backend, and displays responses correctly in the deployed environment.
-   **Monitoring**: Monitor frontend performance (e.g., page load times, API call success rates).
-   **Updates**: To update the site, push changes to your Git repository, and your CI/CD pipeline (if configured) will automatically rebuild and deploy the new version.
