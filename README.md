# CheckMate

## Inspiration
While the web has taken us to new heights with its interconnectivity, it has perpetuated a huge problem in the form of misinformation. Its easier than ever to post something without a source and go viral, regardless of the truth to that statement. Therefore, it is now more important than ever that we detect if what we see online is actually true, but there is no easy way to verify what you see without doing in-depth research yourself. We built CheckMate to provide a convenient and accurate way to verify any information you might see online.

## What it does
CheckMate is an easy to use chrome extension that uses AI to fact check your journey through the web. With the click of a button, users can analyze any selected text on your screen with our multilevel, multimodal AI fact checker. Users have the option between 3 different "levels", from a fast fact check to a slower, but much more in-depth cross check.

## How we built it
Our team built CheckMate using a Chrome UI integrated with React on the frontend and a python backend using flask to receive API calls. The data is then sent through a multiple levels of fact checking: using Perplexity to find citations, and then scraping those citations using Selenium and _recursively_ running our own analysis on those sources using Gemini to determine their relevance and legitimacy to supporting or disproving the given query.

## Challenges we ran into
The biggest challenge was the backend, specifically with LLMs, like being unfamiliar with specific capabilities that would have saved us time and effort, and committing time to prompt engineering. Additionally, trying to balance our API usage with functionality proved to be a big task.

## Accomplishments that we're proud of
We are proud to have come up with an idea and built it into an actual, usable product in only 24 hours. 

## What we learned
While we all had some experience with most of the languages and APIs used, we still got significant technical experience integrating it all together.

## What's next for CheckMate
The functionality for CheckMate could definitely be expanded to more than just verifying text through a chrome extension and also tackle analyzing youtube videos or phone audio with additional implementation on, for example, iOS and Android.
