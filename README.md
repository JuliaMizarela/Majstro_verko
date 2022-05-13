# Majstro_verko

A graph-database of subjectively similar cinematographic media. Movies, series and animations connected through common themes (instead of the usual cast, genre, nationality... objective markers). Made in Node4j with a Python driver.


## Motivations

Current media recommendation algorithms seem to have a hard time with subjective experiences such as impact, pacing, dialogue-hevyness, protagonist-likability, story-complexity and many others. Categorizing media in those therms is often a thought-provocative, fresh take on consumed material - for better or worse.  Even when user input is taken into account, it's often not un-skewed enough to account for how main-stream a certain project was, making it un-precise for niche audiences or particular emotions evocated. User-created tags, as seen in Steam video-games categories do offer a way for these more subjective systems to work at scale and are a quite formidable window into the public-perception of a game, but don't seem to participate in the recommendation systems effectively. 

Curating video-games, literature, or even anime, is often a mixed exercise on empathy for the viewer/player/reader and cartography of the proximity between hundreds or thousands of known examples, that take time, patience, and great memory to be efficient. Admittedly, the more coherent a group, the more probable it is that a subjective map such as this is gonna make sense to everyone when navigating from story to story, but having a "starting-template" like this one may be a good way for similar (pun intended) projects to trace their own maps. If this project ever gets to scale, intertwining these maps, checking for meta-similarity, could help create efficient artificially coherent recommendation groups, with much needed user-created input that actually convey user-subjective experience of media, useful for somewhat similar individuals.


## Tech Stack

Initially the tech stack is only Python 3.8.0+ with a Neo4j graph-database, so no-SQL and graphs basics understanding is nice, but maybe only mandatory if forking or adapting the scripts. Python knowledge is mandatory with the scripts as are, but it is plausible to use other language drives with the same database, and Neo4j supports, besides Python, Java, .Net, JS and Go, so possibly any of those could be used.

If the project ever gets to be featured on the web, then it is gonna use vanilla HTML5, CSS3, minimum JS for front and PHP for back, as those are commonly known (or at least readable and adaptable at basic levels) by most developers with any web experience.


## Licensing

The featured media clearly does not belong to this project and each production has it's own copyrighted licenses. This project is similar to a "movie critics database", with clearly subjective opinions that are free to be used for personal enjoyment or similar non-profit projects (see LICENSE for more information).



