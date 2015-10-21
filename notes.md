**nodejs**

  - serverside JavaScript
  - server side build tool
  - package manager includes nodejs, but typically old version
  - remove existing nodejs with ``sudo apt-get purge nodejs``
  - install from PPA with ``curl -sL https://deb.nodesource.com/setup_0.12 | sudo bash -`` and ``sudo apt-get install -y nodejs``
  - asynchronous
  - nodejs comes with its own package manager, ``npm``
    - dependencies of a given package are stored in subdirectory ``node_modules``; can be nested
  - there are also quite a few dependencies that are for building
  
  
****

**bower**

  - client side (in the browser)
  - bower is client side build tool
  - usually bower is installed globally
  - somewhat confusingly, bower is installed with ``npm``
  - [the knowledge base](https://github.com/NLeSC/kb/wiki/Code-Quality) includes the ``.editorconfig`` file that editor programs use to help lay out JavaScript files consistently
  - bower dependencies are in ``bower.json`` located in the root of a project
  - [http://bower.io/](http://bower.io/) lists bower packages
  - the ``bower`` program looks in ``bower.json``, and  retrieves any missing dependencies


****

**editor**

  - atom
    - package manager includes atom, but is generally old version. So install through PPA or download a .deb file
    - start with ``atom .``
  - brackets
  - Eclipse (with plugins)
  - visual studio code
  
  
****

**building JavaScript and serving a webapp**

  - programs: ``gulp`` (or ``grunt``), we chose ``gulp``
  - get started here: [https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md](https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md)
  - lets you automate build tasks, such as
    - transpiling (from TypeScript, CoffeScript, non-default version of JavaScript/ECMAScript)
    - minifying, uglifying
    - running tests
    - conceptually similar to ``make``
    - tasks are defined in a ``gulpfile.js``, located in the root of your project
    - typically installed globally with ``npm install --global gulp``


****

**Setting up a skeleton project (scaffolding)**

  - ``yeoman``
  - typically installed globally with ``npm install --global yo``
  - yeoman uses generators, for example the webapp generator
  - yeoman is typically used at the beginning of a project
  


****

**debugging**

  - debugging is done in the browser using tools that are available there (keybinding to start the developer tools is typically F12)
    - Google Chrome
    - Firefox with Firebug plugin
    - Firefox Developer Edition
    - (Microsoft Edge has a tool called F12)
  - you can use breakpoints and stepping    
    
    
****

**JavaScript libraries**

  - Bootstrap: 
    - library with many UI elements, such as dropdown boxes, buttons, etc. 
    - developed by Twitter
  - d3: visualization
    - developed by Mike Bostock
  - CrossFilter: quick filtering of data sets
    - [http://square.github.io/crossfilter/](http://square.github.io/crossfilter/)
    - dc.js: combination of crossfilter and d3
  
    
****

**Other stuff**

  - SASS
    - 'scriptable CSS'
  - docco: annotated code
  
    


  
