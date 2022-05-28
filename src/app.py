import json
from flask import Flask, jsonify, request;
from flaskext.mysql import MySQL;

from config import config;

app = Flask(__name__);

mysql = MySQL();
mysql.init_app(app);

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor = mysql.get_db().cursor();
        sql = "SELECT codigo, nombre, creditos FROM curso";
        cursor.execute(sql);
        datos = cursor.fetchall();
        cursosList = [];
        for fila in datos:
            curso = {'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]};
            cursosList.append(curso);
        return jsonify({'cursos': cursosList, 'mensaje': "Cursos listados"});
    except Exception as ex:
        print(ex);
        return jsonify({'mensaje': "Error"});

@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = mysql.get_db().cursor();
        sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo = '{0}'".format(codigo);
        cursor.execute(sql);
        datos = cursor.fetchone();
        if datos != None:
            curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]};
            return jsonify({'cursos': curso, 'mensaje': "Curso encontrado"});
        else:
            return jsonify({'mensaje': "Curso no encontrado"});
    except Exception as ex:
        print(ex);
        return jsonify({'mensaje': "Error"});

@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        #print(request.json)
        cursor = mysql.get_db().cursor();
        sql = """INSERT INTO curso (codigo, nombre, creditos)
        VALUES ('{0}', '{1}', '{2}')""".format(request.json['codigo'], 
        request.json['nombre'], request.json['creditos']);
        cursor.execute(sql);
        #Confirma la acción de inserción
        mysql.get_db().commit();
        return jsonify({'mensaje': "Curso registrado."});
    except Exception as ex:
        print(ex);
        errno, strerror = ex.args
        return jsonify({'mensaje': strerror});

@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor = mysql.get_db().cursor();
        sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo);
        cursor.execute(sql);
        mysql.get_db().commit();
        return jsonify({'mensaje': "Curso eliminado."});
    except Exception as ex:
        print(ex);
        errno, strerror = ex.args
        return jsonify({'mensaje': strerror});

@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    try:
        cursor = mysql.get_db().cursor();
        sql = """UPDATE curso SET nombre = '{0}', creditos = '{1}' 
        WHERE codigo ='{2}'""".format(request.json['nombre'], request.json['creditos'],codigo);
        cursor.execute(sql);
        mysql.get_db().commit();
        return jsonify({'mensaje': "Curso actualizado."});
    except Exception as ex:
        print(ex);
        errno, strerror = ex.args
        return jsonify({'mensaje': strerror});

def pagina_not_found(error):
    return "<h1>La página que intentas buscar no existe ...</h1>", 404;

if __name__ == '__main__':
    app.config.from_object(config['development']);
    app.register_error_handler(404,pagina_not_found);
    app.run();