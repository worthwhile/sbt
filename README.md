# sbt
A partial implementation of the solutions by text REST API

Read their docs here: https://www.solutionsbytext.com/solutions/api-integration/

##  Basic Usage

Simply import it and pass the appropriate payload.

    import sbt
    
    data = {
        'phone': '18881234567',
        'securityToken': 'really-long-t0k3n',
        'orgCode': 'abc123'
     }

    response = sbt.Carrier().get(data)
