---
title: Introduction to Maven
layout: default
nav_order: 20
---

# A Brief Overview to Maven

Maven is a build tool centered around the idea that different aspects of a project's build process can be captured as *life cycles* which are sequences of *phases*.

The image below is taken from [this excellent introductory post](https://medium.com/@yetanothersoftwareengineer/maven-lifecycle-phases-plugins-and-goals-25d8e33fa22) and captures the essence nicely: It shows the three life cycles *default* , *clean* and *site*, and the corresponding sequence of phases, whereas the dark blue ones are the most relevant ones.

Note the phase *generate-resources* which can be used to generate data and *process-resources* which is intended to make it ready for packaging.

The `pom.xml` file captures a model of your project. The point that is crucial to the understanding is expressed in the bold statement cited from  https://maven.apache.org/pom.html:

> The Maven POM is big. However, its size is also a testament to its versatility. **The ability to abstract all of the aspects of a project into a single artifact is powerful, to say the least**. Gone are the days of dozens of disparate build scripts and scattered documentation concerning each individual project.

Within a pom.xml you can use any number of Maven plugins to execute code to alter virtually any aspect of your project. Plugins are can do data and code generation, packaging, deployment or alter the `pom.xml` itself.



<img src="images/maven-lifecycles.png" width="900"/>

<sub>Image source: https://medium.com/@yetanothersoftwareengineer/maven-lifecycle-phases-plugins-and-goals-25d8e33fa22</sub>

