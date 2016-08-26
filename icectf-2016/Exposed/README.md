# IceCTF 2016 - Exposed
### Solution By: Nullp0inter

# Solution:
Unfortunately I don't have the actual challenge description right now but it basically told us that there was a site up at exposed.vuln.icec.tf running all sorts of
stuff such as git, nginx, etc. If you visit the site and attempt to the /.git path, the url changes and gives you a little message but it turns out thats not enough
to stop you if you knew what you were looking for. Because this site had a public facing .git directory we can simply git clone the site by doing
`git clone http://exposed.vuln.icec.tf/.git`. Now you have some options here: You can do this challenge the hardway by manually reverting to older revisions
and grepping all files for the flag, but you'll come up with two fake flags that way, ORRRRR the better way is to just use gitg and look through the changes and in
the revision with the comment "added colors", in index.php you can see the flag `IceCTF{secure_y0ur_g1t_repos_pe0ple}`.
