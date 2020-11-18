var dbs = db.getMongo().getDBNames()
for(var i in dbs){
    db = db.getMongo().getDB( dbs[i] );
    if(db.getName() == 'corona'){
        print("dropping " + db.getName() );
        db.dropDatabase();
    }
}

