import subprocess
import os
import csv


type_de_verin="A0"
identifiant="202003201"
temps_de_mesure="20s"
est_conforme  = "\cellcolor{green} OUI"

#####

fh = open('result_test.txt')
fichier=[]
reader = csv.reader(fh, delimiter = ';')
for ligne in reader:
    fichier.append(ligne)

tableau_des_message=[]  

for i in range(len(fichier)):
    nom_du_test1=fichier[i][1] 
    nom_du_test1=nom_du_test1[1:len(nom_du_test1)-1]+ " & "
    nom_du_test=""
    
    for j in range(len(nom_du_test1)):
        A=nom_du_test1[j]
        if A=="_":
            A=" "
        else:
            A=nom_du_test1[j]
        nom_du_test+=A        
    
    conforme=0
    message=fichier[i][2]+"\\\\ "
    if fichier[i][0]=="[v]":
        conforme="\\color[HTML]{34FF34} \\checkmark & "
    else:
        conforme="\\color[HTML]{FE0000} \\ding{55} & "
        est_conforme="\cellcolor{red} NON"
    tableau_des_message.append(nom_du_test+conforme+message)

#####


photo=[["img/photos_legende/verin_avec_legende.jpg","Vue générale"]] #[[chemin,titre]]

nom_du_fichier_tex="rapport.tex"

lettre=["a","b","c","d","e"]
for i in lettre:
    photo.append(["img/photos_legende/"+i+".jpg",i])
    

fichier = open(nom_du_fichier_tex, "w")


#Déclaration des bibliotheques utilisees

fichier.write("\\UseRawInputEncoding \n")
fichier.write("\\documentclass[a4paper,10pt]{article} \n")
fichier.write("\\usepackage[latin1]{inputenc} \n")
fichier.write("\\usepackage[french]{babel} \n")
fichier.write("\\usepackage[T1]{fontenc} \n")
fichier.write("\\usepackage{graphicx} \n")
fichier.write("\\usepackage{amsmath} \n")
fichier.write("\\usepackage{float} \n")
fichier.write("\\usepackage{subcaption} \n")
fichier.write("\\usepackage{geometry} \n")
fichier.write("\\usepackage{pdfpages} \n")
fichier.write("\\usepackage{eurosym} \n")
fichier.write("\\usepackage{textcomp} \n")
fichier.write("\\usepackage{multicol} \n")
fichier.write("\\usepackage{datetime} \n")
fichier.write("\\usepackage{colortbl} \n")
fichier.write("\\usepackage{amssymb} \n")
fichier.write("\\usepackage{pifont} \n")

fichier.write("\\geometry{hmargin=1.5cm,vmargin=1.5cm} \n")
fichier.write("\\newcommand{\\HRule}{\\rule{\\linewidth}{0.5mm}} \n")
fichier.write("\n")
fichier.write("\n")
#Debut du document

fichier.write("\\begin{document} \n")
fichier.write("\n")

#Positionnement des deux logos

fichier.write("\\begin{minipage}{\\linewidth} \n")
fichier.write("\\vspace{-1cm} \n")
fichier.write("\t \\begin{minipage}{0.2\\linewidth} \n")
fichier.write("\t \t \\begin{figure}[H] \n")
fichier.write("\t \t \t \\includegraphics[width=\\linewidth]{img/Logo_ACS.png} \n")
fichier.write("\t \t \\end{figure} \n")
fichier.write("\t \\end{minipage} \n")
fichier.write("\t \\hfill \n")
fichier.write("\t \\begin{minipage}{0.3\\linewidth} \n")
fichier.write("\t \t \\begin{figure}[H] \n")
fichier.write("\t \t \t \\includegraphics[width=\\linewidth]{img/Logo_couleur_RVB.png} \n")
fichier.write("\t \t \\end{figure} \n")
fichier.write("\t \\end{minipage} \n")
fichier.write("\\end{minipage} \n")
fichier.write("\n")

#Titre du rapport de contole

fichier.write("\\begin{center} \n")
fichier.write("\t { \\huge \\bfseries Rapport de contrôle  \\\\[0.4cm] } \n")
fichier.write("\t \\HRule \\\\[0.5cm] \n")
fichier.write("\\end{center}  \n")
fichier.write("\n")

#Section information

fichier.write("\\section*{Informations} \n")
fichier.write("\n")

fichier.write("\\begin{multicols}{2} \n")
fichier.write("\t \\begin{tabular}{l l} \n")
fichier.write("\t \\textbf{Type de vérin} : & " + type_de_verin+" \\\\ \n")
fichier.write("\t \\textbf{Date} : & \\today \\\\ \n")
fichier.write("\t \\textbf{Heure} : & \\currenttime \n")
fichier.write("\t \\end{tabular} \n \n")
fichier.write("\t \\columnbreak \n \n")
fichier.write("\t \\begin{tabular}{l c} \n")
fichier.write("\t \\textbf{Identifiant} :  & " + identifiant +"  \\\\ \n")
fichier.write("\t \\textbf{Conforme} :     & "+ est_conforme +"\\\\ \n")
fichier.write("\t \\textbf{Temps mesure} : & "+ temps_de_mesure + "\n")
fichier.write("\t \\end{tabular} \n")
fichier.write("\\end{multicols} \n \n")



#Partie tableau des test

fichier.write("\\section*{Tableau des test} \n")

#Creation du tableau

fichier.write("\\begin{center} \n")
fichier.write("\\begin{tabular}{l|c|l} \n")
fichier.write("\t \\hline \n")
fichier.write("\t \\textbf{Nom du test} & \\textbf{Conforme} & \\textbf{Message}\\\\ \n")
fichier.write("\t \\hline \n")
for ligne in tableau_des_message:
    fichier.write("\t"+ligne+"\n")
    
fichier.write("\t \\hline \n")
fichier.write("\\end{tabular} \n")
fichier.write("\\end{center} \n \n")



#Partie des photos

fichier.write("\\section*{Photos du contrôle} \n \n")


fichier.write("\\begin{figure}[H] \n")
fichier.write("\\centering \n")
for p in photo:
    fichier.write("\t \\begin{subfigure}[b]{0.3\\textwidth} \n")
    fichier.write("\t \t \\centering \\includegraphics[width=\\textwidth]{"+p[0]+"} \n")
    fichier.write("\t \t \\caption*{"+p[1]+"} \n")
    fichier.write("\t \\end{subfigure} \n")
    fichier.write("\t ~\n")   
fichier.write("\\end{figure} \n")


fichier.write("\\end{document} \n")

fichier.close()

#Compilation du fichier txt en tex 
#le fichier.write("\\UseRawInputEncoding \n") est SUPER important pour pouvoir compiler



a = subprocess.call('pdflatex -interaction=nonstopmode '+nom_du_fichier_tex)
if a == 0 :
     print("Le fichier a bien été généré")
else : 
     print("problème")
  
    
    
#os.remove("rapport.log")
os.remove("rapport.aux")
os.remove("rapport.tex")


