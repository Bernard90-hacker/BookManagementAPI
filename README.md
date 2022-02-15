Cette API est conçue pour gérer les livres d'une bibliothèque.
Voici les résultats que j'obtiens avec les différentes routes:
Pour avoir tous les livres de la bibliothèque:
/GET/livres
{
            "Success": true,
            "livres": [
                        {
                            "Catégorie": 5,
                            "Nom de l'auteur": "Roosevelt",
                            "Nom de l'éditeur": "LaPresse",
                            "date de publication": "Wed, 10 Nov 2021 00:00:00 GMT",
                            "id": 2,
                            "isbn": "AP20211110",
                            "titre": "Apogee du monde"
                        },
                        {
                            "Catégorie": 5,
                            "Nom de l'auteur": "Paul Wilson",
                            "Nom de l'éditeur": "Harmonies",
                            "date de publication": "Sun, 25 Jun 2017 00:00:00 GMT",
                            "id": 3,
                            "isbn": "FK0424",
                            "titre": "Le principe du calme"
                        },
                        {
                            "Catégorie": 6,
                            "Nom de l'auteur": "Dale Carnegie",
                            "Nom de l'éditeur": "La Maison des livres",
                            "date de publication": "Mon, 11 Jun 2001 00:00:00 GMT",
                            "id": 4,
                            "isbn": "CMD6576",
                            "titre": "Comment se faire des amis ? "
                        }
                    ]
}

Sélectionner un livre par son id: /GET/livres/id
D'abord je choisis un id existant dans la table livres(2)
{
    "selected_book": {
        "Catégorie": 5,
        "Nom de l'auteur": "Roosevelt",
        "Nom de l'éditeur": "LaPresse",
        "date de publication": "Wed, 10 Nov 2021 00:00:00 GMT",
        "id": 2,
        "isbn": "AP20211110",
        "titre": "Apogee du monde"
        },
    "selected_id": 2,
    "success": true
}
Ensuite un id qui n'existe pas dans la table livres(1) Ici j'ai capturé l'erreur 404
{
    "Ressource": "Not Found",
    "success": false
}

Passons aux catégories
Ensemble des catégories: /GET/categories
{
    "Categories": [
    {
        "Libellé": "Fiction",
        "id": 1
        },
        {
        "Libellé": "Policier",
        "id": 2
        },
        {
        "Libellé": "Conte",
        "id": 3
        },
        {
        "Libellé": "Harlequin",
        "id": 4
        },
        {
        "Libellé": "Science",
        "id": 5
        },
        {
        "Libellé": "Philosophie",
        "id": 6
    }
    ],
    "success": true
}
Sélectionner une catégorie par son id: 
D'abord un id existant dans la table categories : 5
/GET/categories/5
{
    "Categories": {
    "Libellé": "Science",
    "id": 5
    },
    "selected_id": 5,
    "success": true
}
Ensuite un id n'existant pas dans la table livres : 9
/GET/categories/9
{
    "Ressource": "Not Found",
    "success": false
} 
Capture de l'erreur 404 (Ressource not found)
Passons aux categories des livres:
Les livres de la categorie 5 :/GET/categories/5/livres
{
    "selected_books": [
                        {
                            "Catégorie": 5,
                            "Nom de l'auteur": "Roosevelt",
                            "Nom de l'éditeur": "LaPresse",
                            "date de publication": "Wed, 10 Nov 2021 00:00:00 GMT",
                            "id": 2,
                            "isbn": "AP20211110",
                            "titre": "Apogee du monde"
                        },
                        {
                            "Catégorie": 5,
                            "Nom de l'auteur": "Paul Wilson",
                            "Nom de l'éditeur": "Harmonies",
                            "date de publication": "Sun, 25 Jun 2017 00:00:00 GMT",
                            "id": 3,
                            "isbn": "FK0424",
                            "titre": "Le principe du calme"
                        }
                    ],
    "success": true
}
Les livres de la categorie 6
{
"selected_books": [
    {
    "Catégorie": 6,
    "Nom de l'auteur": "Dale Carnegie",
    "Nom de l'éditeur": "La Maison des livres",
    "date de publication": "Mon, 11 Jun 2001 00:00:00 GMT",
    "id": 4,
    "isbn": "CMD6576",
    "titre": "Comment se faire des amis ? "
    }
],
"success": true
}
Les livres de la catégorie 9 étant donné que cette catégorie n'existe pas
{
    "Ressource": "Not Found",
    "success": false
}