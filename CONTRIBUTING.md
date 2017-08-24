## Preparation

### Fork the buildtest-framework

First, you'll need to fork [buildtest-framework from GitHub](https://github.com/HPC-buildtest/buildtest-framework).

You might need to setup your SSH keys in your profile if you are using ssh option for cloning. For more details on 
setting up SSH keys in your profile, follow instruction found in https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to repository without requesting a credential. If you don't have a Github account, please 
register an account so you can fork this repo.

After creating your fork copy, clone your fork buildtest-framework repo

```bash
git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest-framework.git
```


### Sync devel branch from upstream

The devel from upstream will get Pull Requests from other contributors, inorder to sync your forked repo with upstream, run the commands below:

```bash
cd buildtest-framework
git remote add upstream git@github.com:HPC-buildtest/buildtest-framework.git
git branch devel
git checkout devel
git pull upstream devel
```

### Branch

Please make sure to create a new branch when adding and new feature. Do not push to **master** or **devel** branch on your fork or upstream. 

Create a new branch as follows

```bash
cd buildtest-framework
git checkout devel
git checkout -b featureX
```

Once you are ready to push to your fork repo do the following

```bash
git push origin featureX
```

Once the branch is created in your fork, you can create a PR to the **devel** branch

### Review

Someone from the **buildtest team** will review the PR and get back to you with the feedback. If the reviewer requests some changes, then the user is requested to make changes and update the branch used for sending PR



