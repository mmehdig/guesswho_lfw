#attributes
import re
attributes = ['Male',
 'Asian',
 'White',
 'Black',
 'Baby',
 'Child',
 'Youth',
 'Middle Aged',
 'Senior',
 'Black Hair',
 'Blond Hair',
 'Brown Hair',
 'Bald',
 'No Eyewear',
 'Eyeglasses',
 'Sunglasses',
 'Mustache',
 'Smiling',
 'Frowning',
 'Chubby',
 'Blurry',
 'Harsh Lighting',
 'Flash',
 'Soft Lighting',
 'Outdoor',
 'Curly Hair',
 'Wavy Hair',
 'Straight Hair',
 'Receding Hairline',
 'Bangs',
 'Sideburns',
 'Fully Visible Forehead',
 'Partially Visible Forehead',
 'Obstructed Forehead',
 'Bushy Eyebrows',
 'Arched Eyebrows',
 'Narrow Eyes',
 'Eyes Open',
 'Big Nose',
 'Pointy Nose',
 'Big Lips',
 'Mouth Closed',
 'Mouth Slightly Open',
 'Mouth Wide Open',
 'Teeth Not Visible',
 'No Beard',
 'Goatee',
 'Round Jaw',
 'Double Chin',
 'Wearing Hat',
 'Oval Face',
 'Square Face',
 'Round Face',
 'Color Photo',
 'Posed Photo',
 'Attractive Man',
 'Attractive Woman',
 'Indian',
 'Gray Hair',
 'Bags Under Eyes',
 'Heavy Makeup',
 'Rosy Cheeks',
 'Shiny Skin',
 'Pale Skin',
 "5 o' Clock Shadow",
 'Strong Nose-Mouth Lines',
 'Wearing Lipstick',
 'Flushed Face',
 'High Cheekbones',
 'Brown Eyes',
 'Wearing Earrings',
 'Wearing Necktie',
 'Wearing Necklace']

def parser(sample): 

    # tockenization, normalization
    sample = sample.lower()
    sample = sample.strip('.!')
    sample = sample.replace('hasn\'t', 'has not').replace('isn\'t', 'is not')
    sample = sample.replace(' a ', ' ').replace(' an ', ' ').replace(' the ', ' ')
    sample = sample.replace('not ', 'not_').replace('no ', 'no_')
    sample = sample.replace('wearing ','wearing_')

    if re.match(r'.+hair\sis\snot.+',sample)!=None:
        sample = re.sub(r'.hair\sis\snot.'," not_hair_",sample)
    else:
        sample = re.sub(r'.hair\sis\s'," hair_",sample)

    sample = sample.replace('brown ','brown_').replace('blue ','blue_').replace('blond ',"blond_").replace("black ","black_").replace('gray ','gray_')

    sample_tockenized = sample.split()
    print(sample_tockenized)

    # dictionary


    att_synonym = {a.lower(): [a.lower()] for a in attributes}
    att_antonym = {a.lower(): ['not_'+a.lower(), 'no_'+a.lower()] for a in attributes}


   # some manual lists

   #getting the synonyms from a file
    with open ("att_synonyms.txt","r") as f:
        for line in f:
            synonyms = line.split()
            for i,synonym in enumerate(synonyms):
                synonym = synonym.replace("_"," ")
                att_synonym[synonyms[0].replace("_"," ")] +=[synonyms[i]]


    #getting the antonyms from a file
    with open("att_antonyms.txt",'r') as f2:
        for line in f2:
            antonyms = line.split()
            attribute=antonyms[0]
            for antonym in antonyms[1:]:
                antonym = antonym.replace("_"," ")
                att_antonym[attribute.replace("_"," ")] +=[antonym]

    # parser
    print(len(attributes))
    result = [0] * 73
    print(len(result))
    
    for i,attribute in enumerate(attributes):
        if len([1 for a in att_synonym[attribute.lower()] if a in sample_tockenized]):
            print("the sample has/is", attribute)
            result[i] = 1
        if len([1 for a in att_antonym[attribute.lower()] if a in sample_tockenized]):
            print("the sample has/is not", attribute)
            result[i] = -1
    
    return result
