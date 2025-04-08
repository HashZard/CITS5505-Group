# 👥 GitHub Collaborator Workflow

This document explains how collaborators can contribute to this repository without pushing directly to the `main`
branch.

---

## ✅ 1. Clone the Repository

Use the following command to clone the project to your local machine:

```bash
git clone https://github.com/HashZard/CITS5505-Group.git
cd CITS5505-Group
```

---

## ✅ 2. Create a New Branch

Always create a new branch from `main` before working on a new feature or fix.

Use a descriptive name like:

- `feature/login-page`
- `fix/typo-in-readme`

Example command:

```bash
git checkout -b feature/your-feature-name
```

---

## ✅ 3. Make Changes and Commit

After making your changes, stage and commit them:

```bash
git add .
git commit -m "Add: brief description of your changes"
```

Use meaningful commit messages that describe **what** and **why**.

---

## ✅ 4. Push Your Branch to GitHub

Push your branch to the remote repository:

```bash
git push origin feature/your-feature-name
```

---

## ✅ 5. Open a Pull Request

To merge your changes into the `main` branch:

1. Go to the GitHub repository page
2. Click **"Compare & pull request"**
3. Fill in a title and a short description of your changes
4. Select `main` as the base branch
5. Submit the Pull Request (PR)

> 🔒 You **cannot push directly to `main`**. All changes must be reviewed and approved through a pull request.

---

## 📝 Summary

```bash
# Clone the repo
git clone <repo-url>
cd <repo-folder>

# Create a new branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "Add: my feature"

# Push and create PR
git push origin feature/my-feature
# → Open PR on GitHub
```
