# ACS  
![](doc/img/acs_logo_small.png)  
A software to create a control station in a industrial environment.

# Introduction
 Cet outil permet de photographier un vérin automatiquement, déterminer les composants qui sont censés être installés (configuration souhaitée), analyser les images afin d'obtenir la configuration réelle.  
 
 Ensuite, en analysant les configurations souhaitées et réelles, l'outil est capable de déterminer si le vérin est bon ou si quelque chose s'est mal passé lors de la production (composant non monté sur le vérin ou à la mauvaise place par exemple). 

# Cadre global
Ce projet a été réalisé dans le cadre de l'usine agile 4.0 qui représente une production de vérin dans un but pédagogique. Il est réalisé en coopération avec de nombreuses équipes qui travaillent toutes sur des points particuliers.  

Dans une production de vérins variée (de multiples composants peuvent être ajoutés pour personalliser le vérin), le contrôle de leur configuration avant l'envoi au client est essentiel, d'où cet outil.


# Fonctionnement
Le fonctionnement est détaillé dans la [documentation](doc/intro.md)

# Avancement  
:white_check_mark: Implémentation des fonctionnalités essentielles  
:zzz: Prise de photo automatique par un robot collaboratif (Cette section a été temporairement mise en pause, faute d'accès à la plateforme)  
:white_check_mark: Ecriture d'une documentation
- [ ] Génération d'un rapport clair sur le contrôle d'un vérin
- [ ] Tests de robustesse permettant de s'assurer que l'on puisse détecter les composants malgré les variations de fond  

# Installation
Notez que j'utilise la version `3.6.8` de python. Je vous conseille aussi de créer un environement virtuel. 

1. Ouvrez l'invité de commande dans le dossier de votre choix et créez un dossier
```
mkdir ACS
cd ACS
```

2. Clonez le répertoire 
```
git clone https://github.com/Skeemet/ACS
```

3. Installez les dépendances
```
pip install -r requirements.txt
```
4. Lancer un IDE (exemple visual code)
```
code .
```


# Troubleshouting
Si vous installez à la main les librairies, il ne faut pas oublier d'installer les scripts qui vont avec la librairie _pyzbar_.
```
python -m pip install pyzbar
python -m pip install pyzbar[scripts]
```

De plus, assurez-vous que _Visual C++ Redistributable Packages for Visual Studio 2013_ soit installé. Vous pouvez le téléchargez ici :arrow_forward: [https://www.microsoft.com/fr-fr/download/confirmation.aspx?id=40784 :link:](https://www.microsoft.com/fr-fr/download/confirmation.aspx?id=40784)  

Ajoutez un dossier `actuators/temp`
