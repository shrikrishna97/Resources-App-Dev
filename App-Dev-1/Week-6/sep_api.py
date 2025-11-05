from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_restful import Api, Resource
from sep_models import db, LinkedInProfile
from ddgs import DDGS  # duckduckgo_search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)


# ---------------------------
# Helper Function using ddgs
# ---------------------------
def scrape_linkedin_url(name):
    """Return the first LinkedIn profile URL found using DuckDuckGo."""
    query = f"{name} site:linkedin.com/in/"
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        if results:
            for r in results:
                link = r.get("href") or r.get("link") or r.get("url")
                if link and "linkedin.com/in/" in link:
                    return link
    return None


# ---------------------------
# REST API Resource
# ---------------------------
class LinkedInSearch(Resource):
    def get(self):
        """Get all profiles stored in the database."""
        profiles = LinkedInProfile.query.all()
        return jsonify([
            {"id": p.id, "name": p.name, "linkedin_url": p.linkedin_url}
            for p in profiles
        ])

    def post(self):
        """Search and store a LinkedIn profile."""
        data = request.get_json()
        name = data.get('name')
        if not name:
            return {'error': 'Name is required'}, 400

        profile = LinkedInProfile.query.filter_by(name=name).first()
        if profile:
            return {'message': 'Already exists', 'linkedin_url': profile.linkedin_url}, 200

        linkedin_url = scrape_linkedin_url(name)
        new_entry = LinkedInProfile(name=name, linkedin_url=linkedin_url)
        db.session.add(new_entry)
        db.session.commit()
        return {'name': name, 'linkedin_url': linkedin_url or 'Not found'}, 201

    def put(self):
        """Update a profile by name."""
        data = request.get_json()
        name = data.get('name')
        new_link = data.get('linkedin_url')
        if not name or not new_link:
            return {'error': 'Name and linkedin_url are required'}, 400

        profile = LinkedInProfile.query.filter_by(name=name).first()
        if not profile:
            return {'error': 'Profile not found'}, 404

        profile.linkedin_url = new_link
        db.session.commit()
        return {'message': 'Profile updated successfully'}, 200

    def delete(self):
        """Delete a profile by name."""
        data = request.get_json()
        name = data.get('name')
        if not name:
            return {'error': 'Name is required'}, 400

        profile = LinkedInProfile.query.filter_by(name=name).first()
        if not profile:
            return {'error': 'Profile not found'}, 404

        db.session.delete(profile)
        db.session.commit()
        return {'message': f'Profile {name} deleted successfully'}, 200


api.add_resource(LinkedInSearch, '/api/search')


# ---------------------------
# HTML Routes
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            existing = LinkedInProfile.query.filter_by(name=name).first()
            if not existing:
                linkedin_url = scrape_linkedin_url(name)
                profile = LinkedInProfile(name=name, linkedin_url=linkedin_url)
                db.session.add(profile)
                db.session.commit()
            return redirect(url_for('home'))

    profiles = LinkedInProfile.query.all()
    return render_template('index1.html', profiles=profiles)


@app.route('/update/<int:profile_id>', methods=['POST'])
def update(profile_id):
    profile = LinkedInProfile.query.get(profile_id)
    if profile:
        new_name = request.form.get('new_name')
        new_link = request.form.get('new_link')
        if new_name:
            profile.name = new_name
        if new_link:
            profile.linkedin_url = new_link
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:profile_id>', methods=['POST'])
def delete(profile_id):
    profile = LinkedInProfile.query.get(profile_id)
    if profile:
        db.session.delete(profile)
        db.session.commit()
    return redirect(url_for('home'))


# ---------------------------
# Initialize Database
# ---------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
