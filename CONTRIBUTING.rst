.. _contributing:

============
Contributing
============

First off, thanks for taking the time to contribute!

Contributions are welcome by anybody and everybody. We are not kidding!

The rest of this document will be guidelines to contributing to the project. Remember that these are just guidelines, not rules. Use common sense as much as possible.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests (if necessary). If you have any questions about how to write tests then ask the community.
2. If the pull request adds functionality update the docs where appropriate.
3. Use a `good commit message`_
4. :ref:`Squash your commit <contributing_squash_commit>`

If you have any issues :ref:`Git Hygiene <contributing_git_hygiene>` might help.

.. _good commit message: https://github.com/spring-projects/spring-framework/blob/30bce7/CONTRIBUTING.md#format-commit-messages


Types of Contributions
----------------------

Report Bugs
^^^^^^^^^^^

Report bugs at https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Bugs & Features
^^^^^^^^^^^^^^^

Look through the gitlab issues for bugs or features request.
Anything tagged with "bug" or "enhancement" is open to whoever wants to implement it.

At this point you might want to pop on the #bots and #community-projects channel of the `python developers slack community`_.
Request an `invite`_.

.. _invite: http://pythondevelopers.herokuapp.com/
.. _python developers slack community: https://pythondev.slack.com/

Write Documentation
^^^^^^^^^^^^^^^^^^^

sir-bot-a-lot could always use more documentation, whether as part of the
official sir-bot-a-lot docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
^^^^^^^^^^^^^^^

The best way to send feedback is to file an issue at https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `sir-bot-a-lot` for local development.

1. Fork the `sir-bot-a-lot` repo on gitlab.
2. Clone your fork locally:

   .. code-block:: console

       $ git clone git@gitlab.com:your_name_here/sir-bot-a-lot.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

   .. code-block:: console

       $ mkvirtualenv sir-bot-a-lot
       $ cd sir-bot-a-lot/
       $ python setup.py develop

4. Create a branch for local development:

   .. code-block:: console

       $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox:

   .. code-block:: console

       $ tox

   To get tox, just pip install it into your virtualenv.

6. Commit your changes and push your branch to gitlab:

.. code-block:: console

       $ git add .
       $ git commit -m "Your detailed description of your changes."
       $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the gitlab website.

Git Hygiene
-----------

.. _contributing_git_hygiene:


Squash Commits
^^^^^^^^^^^^^^

.. _contributing_squash_commit:

**DO NOT REBASE HOTFIXES**

As a general rule of thumb, if a commit modifies a previous commit in the same PR, it probably needs to be squashed. That means that a PR may often only be a single commit. This makes rebasing (see below) easier, and keeps the history clean, which can make debugging infinitely easier in the long run. We also don't need records of only fixing whitespace or spelling mistakes in your PR.

- It's fine to make as many commits as you need while you're working on your local branch. Keeping your history clean as you work will probably be much easier than trying to do it all at the end, though.

- If you just want to make a change and have it apply to your last commit, you can use :code:`git commit --amend`. If you want a change to be associated with an older commit, you can use :code:`git commit -i HEAD~3` (where `3` is the number of commits to rebase). You can also use :code:`git log` to find a commit's hash and :code:`git rebase -i <commit hash>` (the commit should be the one PRIOR to the commit you want to modify).

- Interactive rebase :code:`git rebase -i` will open your default editor in which you can replace :code:`pick` with :code:`fixup` or `f` to combine commits (you can also use this to reorder commits, mark commits to edit their commit messages, and other powerful tools which are explained in the file itself). Save the changes, and git will execute the rebase.

After rebasing, if your branch is already pushed up to GitLab, you'll have to force push the changes using :code:`git push -f`, since the history has changed.

Do you have any questions ?

    *When in doubt, ask me. - @skift*

**Warning:** Only rebase your own branches.

Handling Merge Conflicts
^^^^^^^^^^^^^^^^^^^^^^^^

Occasionally a Pull Request will have Merge Conflicts. **Do not merge master into your branch.** Instead, make sure your :code:`master` branch is up to date:

.. code-block:: console

   $ git checkout master
   $ git pull

Then rebase your branch on :code:`master`:

.. code-block:: console

   $ git checkout _my-branch_
   $ git rebase master

If there are any conflicts you need to resolve, it will suspend the rebase for you to fix them. Then do:

.. code-block:: console

   $ git add .
   $ git rebase --continue


It will do one round of conflict-checking for each commit in your branch, so keeping your history clean will make rebasing much easier. When the rebase is done, your branch will be up to date with master and ready to issue a PR if you are.
