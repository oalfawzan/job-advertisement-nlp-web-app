from flask import Flask, render_template, request, redirect
from gensim.models.fasttext import FastText
import pandas as pd
import pickle
import os
from bs4 import BeautifulSoup

def gen_docVecs(wv,tk_txts): # generate vector representation for documents
    docs_vectors = pd.DataFrame() # creating empty final dataframe
    #stopwords = nltk.corpus.stopwords.words('english') # if we haven't pre-processed the articles, it's a good idea to remove stop words

    for i in range(0,len(tk_txts)):
        tokens = tk_txts[i]
        temp = pd.DataFrame()  # creating a temporary dataframe(store value for 1st doc & for 2nd doc remove the details of 1st & proced through 2nd and so on..)
        for w_ind in range(0, len(tokens)): # looping through each word of a single document and spliting through space
            try:
                word = tokens[w_ind]
                word_vec = wv[word] # if word is present in embeddings(goole provides weights associate with words(300)) then proceed
                temp = temp.append(pd.Series(word_vec), ignore_index = True) # if word is present then append it to temporary dataframe
            except:
                pass
        doc_vector = temp.sum() # take the sum of each column
        docs_vectors = docs_vectors.append(doc_vector, ignore_index = True) # append each document value to the final dataframe
    return docs_vectors

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/accounting_finance')
def accounting_finance():
    return render_template('accounting_finance.html')

@app.route('/engineering')
def engineering():
    return render_template('engineering.html')

@app.route('/healthcare_nursing')
def healthcare_nursing():
    return render_template('healthcare_nursing.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<folder>/<filename>')
def job(folder, filename):
    return render_template('/' + folder + '/' + filename + '.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        f_title = request.form['title']
        f_company = request.form['company']
        f_content = request.form['description']

        if request.form['button'] == 'Classify':

            tokenized_data = f_content.split(' ')

            jobsFT = FastText.load("desc_FT.model")
            jobsFT_wv= jobsFT.wv

            jobsFT_dvs = gen_docVecs(jobsFT_wv, [tokenized_data])

            pkl_filename = "descFT_LR.pkl"
            with open(pkl_filename, 'rb') as file:
                model = pickle.load(file)

            y_pred = model.predict(jobsFT_dvs)
            y_pred = y_pred[0]

            return render_template('admin.html', prediction=y_pred, title=f_title, company=f_company, description=f_content)
            
        elif request.form['button'] == 'Save':
            # First check if the recommended category is empty
            cat_recommend = request.form['category']
            if cat_recommend == '':
                return render_template('admin.html', prediction=cat_recommend, title=f_title, company=f_company, description=f_content, category_flag='Recommended category must not be empty.')

            elif cat_recommend not in ['Accounting_finance', 'Engineering', 'Healthcare_Nursing', 'Sales']:
                return render_template('admin.html', prediction=cat_recommend, title=f_title, company=f_company, description=f_content, category_flag='Recommended category must belong to: Accounting_Finance, Engineering, Healthcare_Nursing, Sales.')

            else:

                # First read the html template
                soup = BeautifulSoup(open('templates/article_template.html'), 'html.parser')
                    
                # Then adding the title and the content to the template
                # First, add the title
                div_page_title = soup.find('div', { 'class' : 'title' })
                title = soup.new_tag('h1', id='data-title')
                title.append(f_title)
                div_page_title.append(title)

                div_page_company = soup.find('div', { 'class' : 'company' })
                company = soup.new_tag('h1', id='data-company')
                company.append(f_company)
                div_page_company.append(company)

                # Second, add the content
                div_page_content = soup.find('div', { 'class' : 'data-job' })
                content = soup.new_tag('p')
                content.append(f_content)
                div_page_content.append(content)

                # Finally write to a new html file
                filename = ''.join(e for e in f_title if e.isalnum())
                filename =  cat_recommend + '/' + filename + ".html"
                with open("templates/" + filename, "w", encoding='utf-8') as file:
                    print(filename)
                    file.write(str(soup))

                # Redirect to the newly-generated news article
                return redirect('/' + filename.replace('.html', ''))

    else:
        return render_template('admin.html')