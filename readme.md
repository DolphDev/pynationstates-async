This is an alpha - early stage library. Mostly mean't to keep what it can of pynationstates interface while providing a async version.

this is being written 

The library has two main modes - burst and limited

notes

burst mode means any number of requests can happen at the same time, outside of trivia and basically instant rate limit checks they will happen simulatously. the drawback is (atleast for now) is the ratelimiter cannot really account for this and it makes the rate limit tracker unreliable (since the latest request sets the x-ratelimit-requests-seen, simulatanous requests will all start with 0 and last request to fish will set the xrls)