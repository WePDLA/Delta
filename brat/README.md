# Akaros标注系统 #

## 说明 ##

该系统是在[brat homepage][brat]的基础上进行开发操作，里面添加许多许多功能，大部分功能为了便于我们系统的使用，比如多用户操作
、数据库操作（使用的sqlite）、自动标注等。当然很多功能不能一般话，它只是根据我们团队自己的需要进行操作的，因此，如果你git clone运行可能并不如你所需要的情况
，我们在后续过程中，如果条件允许，我们将对该系统进行更近一步的开发，便于它一般话，而不是针对具体的项目进行。

## 操作 ##

### 启动方式 ### 
先启动standalone.py 便可标注，该方式更brat操作一样，更多请查看brat 文档。
自动标注，在另一个控制中启动web_server.py ，便可。

## Documentation ##

In an attempt to keep all user-facing documentation in one place, please visit
the [brat homepage][brat] which contains extensive documentation and examples
of how to use and configure brat. We apologise for only providing minimal
documentation along with the installation package but the risk of having
out-dated documentation delivered to our end-users is unacceptable.

If you find bugs in your brat installation or errors in the documentation,
please file an issue at our [issue tracker][brat_issues] and we will strive to
address it promptly.

[brat]:         http://brat.nlplab.org
[brat_issues]:  https://github.com/nlplab/brat/issues

## About brat ##

*brat* (brat rapid annotation tool) is based on the [stav][stav] visualiser
which was originally made in order to visualise
[BioNLP'11 Shared Task][bionlp_2011_st] data. brat aims to provide an
intuitive and fast way to create text-bound and relational annotations.
Recently, brat has been widely adopted in the community. It has been used to
create well-over 50,000 annotations by the [Genia group][genia] and several
other international research groups for a number of annotation projects.

[stav]:             https://github.com/nlplab/stav/
[bionlp_2011_st]:   http://2011.bionlp-st.org/
[genia]:            http://www.geniaproject.org/

brat aims to overcome short-comings of previous annotation tools such as:

* De-centralisation of configurations and data, causing synchronisation issues
* Annotations and related text not being visually adjacent
* Complexity of set-up for annotators
* Etc.

brat does this by:

* Data and configurations on a central web server (as Mark Twain said:
    "Put all your eggs in one basket, and then guard that basket!")
* Present text as it would appear to a reader and maintain annotations close
    to the text
* Zero set-up for annotators, leave configurations and server/data maintenance
    to other staff

## License ##

brat itself is available under the permissive [MIT License][mit] but
incorporates software using a variety of open-source licenses, for details
please see see LICENSE.md.

[mit]:  http://opensource.org/licenses/MIT

## Citing ##

If you do make use of brat or components from brat for annotation purposes,
please cite the following publication:

    @inproceedings{,
        author      = {Stenetorp, Pontus and Pyysalo, Sampo and Topi\'{c}, Goran
                and Ohta, Tomoko and Ananiadou, Sophia and Tsujii, Jun'ichi},
        title       = {{brat}: a Web-based Tool
                for {NLP}-Assisted Text Annotation},
        booktitle   = {Proceedings of the Demonstrations Session
                at {EACL} 2012},
        month       = {April},
        year        = {2012},
        address     = {Avignon, France},
        publisher   = {Association for Computational Linguistics},
    }

If you make use of brat or its components solely for visualisation purposes,
please cite the following publication:

    @InProceedings{stenetorp2011supporting,
      author    = {Stenetorp, Pontus and Topi\'{c}, Goran and Pyysalo, Sampo
          and Ohta, Tomoko and Kim, Jin-Dong and Tsujii, Jun'ichi},
      title     = {BioNLP Shared Task 2011: Supporting Resources},
      booktitle = {Proceedings of BioNLP Shared Task 2011 Workshop},
      month     = {June},
      year      = {2011},
      address   = {Portland, Oregon, USA},
      publisher = {Association for Computational Linguistics},
      pages     = {112--120},
      url       = {http://www.aclweb.org/anthology/W11-1816}
    }

Lastly, if you have enough space we would be very happy if you also link to
the brat homepage:

    ...the brat rapid annotation tool\footnote{
        \url{http://brat.nlplab.org}
    }

## Contributing ##

As with any software brat is under continuous development. If you have
requests for features please [file an issue][brat_issues] describing your
request. Also, if you want to see work towards a specific feature feel free to
contribute by working towards it. The standard procedure is to fork the
repository, add a feature, fix a bug, then file a pull request that your
changes are to be merged into the main repository and included in the next
release. If you seek guidance or pointers please notify the brat developers
and we will be more than happy to help.

If you send a pull request you agree that the code will be distributed under
the same license as brat (MIT). Additionally, all non-anonymous contributors
are recognised in the CONTRIBUTORS.md file.

## Contact ##

For help and feedback please contact the authors below, preferably with all on
them on CC since their responsibilities and availability may vary:

* Goran Topić       &lt;amadanmath gmail com&gt;
* Sampo Pyysalo     &lt;sampo.pyysalo gmail com&gt;
* Pontus Stenetorp  &lt;pontus stenetorp se&gt;
