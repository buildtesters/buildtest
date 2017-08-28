Want to contribute back to this project and make this project a success? 
Please follow the instructions below, we would love to get your feedback to 
improve this
project.

## Preparation

### Fork the buildtest-configs

First, you will need to fork [buildtest-configs from GitHub](https://github.com/HPC-buildtest/buildtest-configs).

You might need to setup your SSH keys in your profile if you are using ssh 
option for cloning. For more details on setting up SSH keys in your profile, 
follow instruction found in 
https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to repository without requesting a 
credential. If you dont have a Github account, please register an account so 
you can fork this repo.

After creating your fork copy, clone your fork buildtest-framework repo

```bash
git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest-configs.git
```


### Sync devel branch from upstream

The devel from upstream will get Pull Requests from other contributors, inorder
 to sync your forked repo with upstream, run the commands below:

```bash
cd buildtest-configs
git remote add upstream git@github.com/HPC-buildtest/buildtest-configs.git
git branch devel
git checkout devel
git fetch upstream
git pull upstream devel
```

Once the changes are pulled locally you can sync devel branch in your 
fork with upstream

```bash
git checkout devel
git push origin devel
```

Do this same operation with master if you want to sync it with upstream repo

### Branch

Please make sure to create a new branch when adding and new feature. Do not push 
to **master** or **devel** branch on your fork or upstream. 

Create a new branch as follows

```bash
cd buildtest-configs
git checkout devel
git checkout -b featureX
```

Once you are ready to push to your fork repo do the following

```bash
git push origin featureX
```

Once the branch is created in your fork, you can create a PR to the **devel** branch.


### Review

Someone from the **buildtest team** will review the PR and get back to you with 
the feedback. If the reviewer requests some changes, then the user is requested 
to make changes and update the branch used for sending PR

If a PR is closed and you want to make slight adjustment, just open the PR and 
make the change in your branch. If everything looks fine and PR is merged, you 
can delete your local branch.
