<h1 align="center">🎬 MovieProject</h1>

<p align="center">
  A movie tracking and rating application project built with Python.
</p>

<p align="center">
  Build your collection • Rate movies • Track your cinematic journey
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&height=100&color=gradient" width="100%">

## 🚀 Features

### ✅ Current Functionality

- Add movies to a personal collection
- Delete movies from the collection
- Get stats on average rating, best and worst rated movies.
- Search movies by title
- Filter movies by criteria
- Generate random movie suggestions
- Update database with personal ratings and notes
- Display movie collection in a website output  

<img src="https://capsule-render.vercel.app/api?type=rect&height=2&color=0:8A2BE2,100:FF4ECD" width="100%">

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| SQLAlchemy | Database ORM |
| REST API | Movie data fetching |
| HTML5 / CSS3 | Frontend development |

<img src="https://capsule-render.vercel.app/api?type=rect&height=2&color=0:8A2BE2,100:FF4ECD" width="100%">

## 📁 Project Structure

```bash
MovieProject/
│
├── README.md
├── .gitignore
├── requirements.txt
├── main.py
│
├── data/
│    └── movies.db
│
├── movie_storage/
│   ├── __init__.py
│   ├── movie_storage_sql.py
│   └── movie_storage.py  
│
├── api/
│   ├── __init__.py
│   └── omdb_api.py
│
├── web/
│   ├── html_generator.py
│   ├── templates/
│   │   └── index_template.html
│   ├── static/
│   │   ├── style.css
│   │   └── index.html         # generated output
│
├── utils/
│   ├── __init__.py
│   └── utilities.py
```

<img src="https://capsule-render.vercel.app/api?type=rect&height=2&color=0:8A2BE2,100:FF4ECD" width="100%">

## 🚧 Development Status

### ✅ Completed

- Core CRUD functionality
- Search and filtering system
- Random movie recommendation feature
- Stats and rating histogram generation 
- SQL database integration
- External movie API integration
- Frontend website implementation
<br>

<img src="https://capsule-render.vercel.app/api?type=rect&height=2&color=0:8A2BE2,100:FF4ECD" width="100%">

## 🔮 Future Improvements

Planned features for future versions include:

- User profiles
- Advanced filtering and sorting

<img src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color=gradient" width="100%">
