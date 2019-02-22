# GUIDELINES FOR DEVELOPMENT

This project is prone to be developped by several developpers, so we agreed on some basic rules...

## GENERAL 

- we try to comment and document in english
- check out our ["project" boards](https://github.com/co-demos/toktok/projects) to have an idea about the priorities we collectively decided to work on.
- "see something, say something" : open new issues when you see problems needing to be solved. Add tags and referees if possible
- document your own issues with everything you have : images, references, snippets, etc... 
- we update the `README.md` and the `GUIDELINES_DEV.md` directly on github.
- for the markdown files try to [follow those advices](http://www.cirosantilli.com/markdown-style-guide/#dollar-signs-in-shell-code)...

## PYTHON 

- comment your code
- factorize what you can 


## SWAGGER

- eeeeeh... we don't know yet but the actual swagger lacks some swag ...


## GIT MANAGEMENT

We are following this git principles : [link to blog](https://guillim.github.io/git/2018/04/24/Git-workflow.html). In brief : 
- there are 2 main branches : `master` and `develop`
- new features must be code reviewed and then (if accepted) pulled into the branch `develop`
- once every new feature is accepted and merged into `develop`, `develop` must be merged into `master` to constitute a new release

Please follow those rules when developping new features : 
- locally : create a new branch (f.i. `mypseudo_mynewfeature`) to work on your own feature(s)
- before pushing your changes pull the remote `develop` branch to be merged with your changes in `mypseudo_mynewfeature` branch (so to be sure the features you just developped are compatible with the checked/reviewed `develop` branch):
>
  ```bash
  git pull origin develop
  ```
- push your branch to the remote repo (github repo) : 
  > 
    ```bash
    git push origin <mypseudo_mynewfeature>
    ```
- ask for a pull request on Github from `mypseudo_mynewfeature` branch to `develop` branch
- someone else must be assigned as a code reviewer, whose in charge to accept your code changes and merge
- once accepted / reviewed delete `mypseudo_mynewfeature` from repo to keep the branches clean
- once everything is clean maintainers will pull the updated `develop` branch to `master`
