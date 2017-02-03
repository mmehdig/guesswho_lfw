# Guess Who (A game on LFW)
[The Guess who!](https://en.wikipedia.org/wiki/The_Guess_Who) is a two player game which one participant choose a face and other person guess which face has been chosen. In this version, the computer will guess who, while human player choose the picture and describes it.

We are using the Labeled Faces in Wild (LFW) for training:

    @TechReport{LFWTech,
      author =       {Gary B. Huang and Manu Ramesh and Tamara Berg and
                      Erik Learned-Miller},
      title =        {Labeled Faces in the Wild: A Database for Studying
                      Face Recognition in Unconstrained Environments},
      institution =  {University of Massachusetts, Amherst},
      year =         2007,
      number =       {07-49},
      month =        {October}
    }

We also train the lexical descriptors from Kumar et al. (2009) connected to these images:

    @inproceedings{kumar2009attribute,
      title={Attribute and simile classifiers for face verification},
      author={Kumar, Neeraj and Berg, Alexander C and Belhumeur, Peter N and Nayar, Shree K},
      booktitle={2009 IEEE 12th International Conference on Computer Vision},
      pages={365--372},
      year={2009},
      organization={IEEE}
    }

To create the embeddings of the faces we use a model from OpenFace:

    @techreport{amos2016openface,
      title={OpenFace: A general-purpose face recognition
      library with mobile applications},
      author={Amos, Brandon and Bartosz Ludwiczuk and Satyanarayanan, Mahadev},
      year={2016},
      institution={CMU-CS-16-118, CMU School of Computer Science},
}