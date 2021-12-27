This repository contains python scripts, that retrieves information from RP Data website.
<br><br>
Since accessing information requires logging into our account, a work-around was developed. After logging into the account, each page's sources code will be saved locally in a folder, with a specific string format, using an HTTP extension.
<br><br>
Now when the script get executed, it will look for all the files with a pre-defined format and extract the customer and property data in a tabular form in another folder locally.
