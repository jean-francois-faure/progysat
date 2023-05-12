# Progysat

## Configuration

Le site est globalement configurable à l'URL [http://adresse-du-site.fr]/admin.

De nombreux éléments contiennent un champ `slug`, cela correspond à un champ technique, qui doit être unique par type
d'élément. En général, c'est le nom de l'élément, en anglais, en miniscule.

### Les ressources

Depuis le menu de gauche, il y a un sous-menu "Ressources". Ce sous-menu possède trois éléments :
ressources, thématiques et types de ressources.

A priori, les thématiques sont fixes. En tout cas, d'éventuels ajout ne bénéficieraient pas de logo. Les types de
ressources sont plus flexibles car il n'y a pas d'image associée et peuvent donc être configués.

Une ressource doit avoir un fichier lié ou un lien.

### Les actualités

De la même manière, les actualités sont configurés dans le sous-menu Actualités.

### Pays, profils et zones du monde

Les pays, profils et zones du monde sont configurables dans le sous-menu "Général".

De la même manière que les thématiques de ressources, les zones du monde ne sont pas prévues pour être changées, hormis
leur nom.

### Utilisateurs admin

La gestion des utilisateurs se fait depuis le sous-menu Paramètres, puis Utilisateurs. Le plus simple est ensuite de
donner tous les droits aux administrateurs. Depuis l'édition ou l'ajout d'un utilisateur, aller dans l'onglet Rôles, et
cocher toutes les cases.

### Les pages annexes (mentions légales, données personnelles)

Ces pages peuvent être ajoutées / modifiées en créant / modifiant une page de contenu avec comme slug :

- `mentions-legales` pour les mentions légales
- `donnees-personnelles` pour les données personnelles
