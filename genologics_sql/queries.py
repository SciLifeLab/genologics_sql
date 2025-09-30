from genologics_sql.tables import *

from sqlalchemy import text

def get_last_modified_projects(session, interval="2 hours"):
    """gets the project objects last modified in the last <interval>

    :query: select * from project where age(lastmodifieddate)< '1 hour'::interval;

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records

    """
    txt="age(now(),lastmodifieddate)< '{int}'::interval".format(int=interval)
    return session.query(Project).filter(text(txt)).all()

def get_last_modified_project_udfs(session, interval="2 hours"):
    """gets the project objects that have a udf last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records

    """
    query="select pj.* from project pj \
           inner join entityudfstorage eus on pj.projectid = eus.attachtoid \
           where eus.attachtoclassid = 83 and age(now(), eus.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()


def get_last_modified_project_sample_udfs(session, interval="2 hours"):
    """gets the project objects that have sample udfs last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    query= "select distinct pj.* from project pj \
            inner join sample sa on sa.projectid=pj.projectid \
            inner  join processudfstorage pus on sa.processid=pus.processid \
            where age(now(), pus.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()

def get_last_modified_project_artifacts(session, interval="2 hours"):
    """gets the project objects that have artifacts last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    query= "select distinct pj.* from project pj \
            inner join sample sa on sa.projectid=pj.projectid \
            inner join artifact_sample_map asm on sa.processid=asm.processid \
            inner join artifact art on asm.artifactid=art.artifactid \
            where age(now(), art.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()

def get_last_modified_project_artifact_udfs(session, interval="2 hours"):
    """gets the project objects that have artifact udfs last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    query= "select distinct pj.* from project pj \
            inner join sample sa on sa.projectid=pj.projectid \
            inner join artifact_sample_map asm on sa.processid=asm.processid \
            inner join artifactudfstorage aus on asm.artifactid=aus.artifactid \
            where age(now(), aus.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()

def get_last_modified_project_containers(session, interval="2 hours"):
    """gets the project objects that have containers last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    query= "select distinct pj.* from project pj \
            inner join sample sa on sa.projectid=pj.projectid \
            inner join artifact_sample_map asm on sa.processid=asm.processid \
            inner join containerplacement cpl on asm.artifactid=cpl.processartifactid \
            inner join container ct on cpl.containerid=ct.containerid \
            where age(ct.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()

def get_last_modified_project_processes(session, interval="2 hours"):
    """gets the project objects that have containers last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    query= "select distinct pj.* from project pj \
            inner join sample sa on sa.projectid=pj.projectid \
            inner join artifact_sample_map asm on sa.processid=asm.processid \
            inner join processiotracker pit on asm.artifactid=pit.inputartifactid \
            inner join process pro on pit.processid=pro.processid \
            where age(now(), pro.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()

def get_last_modified_project_process_udfs(session, interval="2 hours"):
    """gets the project objects that have containers last modified in the last <interval>

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    query= "select distinct pj.* from project pj \
            inner join sample sa on sa.projectid=pj.projectid \
            inner join artifact_sample_map asm on sa.processid=asm.processid \
            inner join processiotracker pit on asm.artifactid=pit.inputartifactid \
            inner join process pro on pit.processid=pro.processid \
            inner join processudfstorage pus on pro.processid=pus.processid \
            where age(now(), pus.lastmodifieddate) < '{int}'::interval;".format(int=interval)
    return session.query(Project).from_statement(text(query)).all()


def get_last_modified_projectids(session, interval="2 hours"):
    """gets all the projectids for which any part has been modified in the last interval

    :param session: the current SQLAlchemy session to the database
    :param interval: str Postgres-compliant time string
    :returns: List of Project records
    """
    projectids=set()
    for project in get_last_modified_projects(session, interval):
        projectids.add(project.luid)

    for project in get_last_modified_project_udfs(session, interval):
        projectids.add(project.luid)

    for project in get_last_modified_project_sample_udfs(session, interval):
        projectids.add(project.luid)

    for project in get_last_modified_project_containers(session, interval):
        projectids.add(project.luid)

    for project in get_last_modified_project_processes(session, interval):
        projectids.add(project.luid)

    for project in get_last_modified_project_process_udfs(session, interval):
        projectids.add(project.luid)

    return projectids


def get_last_modified_processes(session, ptypes, interval="24 hours"):
    """gets all the processes of the given <type> that have been modified
    or have a udf modified in the last <interval>

    :param session: the current SQLAlchemy session to the db
    :param ptypes: the LIST of process type ids to be returned
    :param interval: the postgres compliant interval of time to search processes in.

    """
    query= "select distinct pro.* from process pro \
            inner join processudfstorage pus on pro.processid=pus.processid \
            where (pro.typeid in ({typelist}) \
            and age(now(), pus.lastmodifieddate) < '{int}'::interval) \
            or \
            (age(now(), pro.lastmodifieddate) < '{int}'::interval \
            and pro.typeid in ({typelist}));".format(int=interval, typelist=",".join([str(x) for x in ptypes]))
    return session.query(Process).from_statement(text(query)).all()

def get_processes_in_history(session, parent_process, ptypes, sample=None):
    """returns all the processes that are found in the history of parent_process
    AND are of type ptypes

    :param session: the current SQLAlchemy session to the db
    :param parent_process: the id of the parent_process
    :param ptypes: the LIST of process type ids to be returned
    :param sample: if defined, filter artifacts that match the correct sample

    """
    qar=["select distinct pro.* from process pro \
            inner join processiotracker pio on pio.processid=pro.processid \
            inner join outputmapping om on om.trackerid=pio.trackerid \
            inner join artifact_ancestor_map aam on pio.inputartifactid=aam.ancestorartifactid\
            inner join processiotracker pio2 on pio2.inputartifactid=aam.artifactid \
            inner join process pro2 on pro2.processid=pio2.processid "]
    if sample:
        qar.append("inner join artifact_sample_map asm on asm.artifactid=pio.inputartifactid ")
    qar.append("where pro2.processid={parent} and pro.typeid in ({typelist}) ")
    if sample:
        qar.append("and asm.processid = {sampleid}".format(sampleid=sample))
    qar.append(";")
    query=''.join(qar).format(parent=parent_process, typelist=",".join([str(x) for x in ptypes]))
    return session.query(Process).from_statement(text(query)).all()

def get_children_processes(session, parent_process, ptypes, sample=None, orderby=None):
    """returns all the processes that are found in the children of parent_process
    AND are of type ptypes

    :param session: the current SQLAlchemy session to the db
    :param parent_process: the id of the parent_process
    :param ptypes: the LIST of process type ids to be returned

    """

    qar1=[   """select pro.* from process pro 
            inner join processiotracker piot on piot.processid=pro.processid 
            inner join artifact_ancestor_map aam on aam.artifactid=piot.inputartifactid 
            inner join outputmapping om on aam.ancestorartifactid=om.outputartifactid
            inner join processiotracker piot2 on piot2.trackerid=om.trackerid """]
    qar2=[  """select pro.* from process pro 
            inner join processiotracker piot on piot.processid=pro.processid 
            inner join outputmapping om on piot.inputartifactid=om.outputartifactid
            inner join processiotracker piot2 on piot2.trackerid=om.trackerid """]
    if sample:
        qar1.append("inner join artifact_sample_map asm on asm.artifactid=piot.inputartifactid ")
        qar2.append("inner join artifact_sample_map asm on asm.artifactid=piot.inputartifactid ")
    qar1.append("where piot2.processid={parent} and pro.typeid in ({typelist}) ")
    qar2.append("where piot2.processid={parent} and pro.typeid in ({typelist}) ")
    if sample:
        qar1.append("and asm.processid = {sampleid} ".format(sampleid=sample))
        qar2.append("and asm.processid = {sampleid} ".format(sampleid=sample))
    if orderby:
        qar2.append("order by {}".format(orderby))

    query="{} union {};".format(''.join(qar1), ''.join(qar2)).format(parent=parent_process, typelist=",".join([str(x) for x in ptypes]))
    return session.query(Process).from_statement(text(query)).all()


def get_all_steps_for_workflow(session, workflow):
    """returns all the steps used in a workflow in order

    :param session: the current SQLAlchemy session to the db
    :param workflow: the name of the workflow
    :returns: List of steps in order in a workflow. The fields returned are protocolstep name, protocolstep id,
                protocol name and stageindex which gives the order of the step in the workflow.

    """
    query = f"select pst.name, pst.stepid, lp.protocolname, stg.stageindex \
           from labworkflow lwf, workflowsection ws, labprotocol lp, protocolstep pst, stage stg \
           where ws.workflowid=lwf.workflowid and ws.protocolid=lp.protocolid and lp.protocolid=pst.protocolid \
           and ws.sectionid=stg.membershipid and pst.stepid=stg.stepid \
           and lwf.workflowname='{workflow}' \
           order by stg.stageindex;"

    return session.execute(text(query)).all()


def get_all_samples_in_a_workflow(session, workflow):
    """returns all the samples waiting in a protocolstep in a workflow

    :param session: the current SQLAlchemy session to the db
    :param workflow: the id of the workflow
    :returns: List of samples in a workflow. The fields returned are artifactid, samplename, stepid of the protocolstep,
                projectid, generatedbyid
    """

    query = f"select distinct(st.artifactid), sa.name, sa.sampleid, stg.stepid, sa.projectid, st.generatedbyid \
              from stagetransition st, stage stg, workflowsection wfs, protocolstep pst, labprotocol lpt, \
                labworkflow lwf, artifact_sample_map asm, sample sa \
              where st.stageid=stg.stageid and stg.membershipid=wfs.sectionid \
              and wfs.workflowid=lwf.workflowid and wfs.protocolid=lpt.protocolid \
              and st.artifactid=asm.artifactid and asm.processid=sa.processid and st.workflowrunid > 0 \
              and lwf.workflowstatus='ACTIVE' and lwf.workflowname='{workflow}';"

    return session.execute(text(query)).all()


def get_udfs_from_sample(session, sampleid, udf_list):
    """returns all values from the given list of udfs which are directly connected to a sample.
        It does not return the udfs from protocol steps.

    :param session: the current SQLAlchemy session to the db
    :param sampleid: sampleid from sample table
    :param udf_list: the list of udf names to be searched. If the list is empty or None, all UDFs are returned.
    :returns: List of sample udf values
    """
    add_udf_to_query = ""
    if udf_list:
        add_udf_to_query = " and udfname in ('{}')".format("', '".join(udf_list))

    query = f"select udfname, udfvalue, udfunitlabel \
              from sample_udf_view \
              where sampleid={sampleid}{add_udf_to_query};"

    return session.execute(text(query)).all()


def get_sample_udfs_from_step(session, sampleid, stepid, udf_list):
    """returns all values of udfs of a sample from a particular step in a protocol.

    :param session: the current SQLAlchemy session to the db
    :param sampleid: sampleid from sample table
    :param stepid: the id of the protocolstep
    :param udf_list: the name of the udf to be retrieved
    """
    udf_list_str= " ('{}')".format("', '".join(udf_list))
    query = f"select udfname, udfvalue, udfunitlabel \
            from artifact_udf_view auv, protocolstep pst, sample sa, processoutputtype pot, artifact art \
            where pst.processtypeid=pot.processtypeid and pot.typeid=art.processoutputtypeid and sa.name=art.name \
            and art.artifactid=auv.artifactid and pst.stepid={stepid} and sa.sampleid={sampleid} and auv.udfname in {udf_list_str};"

    return session.execute(text(query)).all()


def get_udfs_from_project(session, projectid, udf_list):
    """returns all values from the given list of udfs which are directly connected to a project.
        It does not return the udfs from protocol steps.

    :param session: the current SQLAlchemy session to the db
    :param projectid: projectid from project table
    :param udf_list: the list of udf names to be searched. If the list is empty or None, all UDFs are returned.
    :returns: List of project udf values
    """
    add_udf_to_query = ""
    if udf_list:
        add_udf_to_query = " and udfname in ('{}')".format("', '".join(udf_list))

    query = f"select euv.udfname, euv.udfvalue, euv.udfunitlabel, pr.name \
              from entity_udf_view euv, project pr \
              where euv.attachtoid=pr.projectid and \
              euv.attachtoid={projectid}{add_udf_to_query};"

    return session.execute(text(query)).all()


def get_reagentlabel_for_sample(session, sampleid):
    """returns the reagentlabel for a sample

    :param session: the current SQLAlchemy session to the db
    :param sampleid: sampleid from sample table
    :returns: reagentlabel for the sample
    """
    query = f"select distinct(rl.name) \
              from reagentlabel rl, artifact_label_map alm, sample sa, artifact art \
              where alm.labelid=rl.labelid and art.artifactid=alm.artifactid \
              and sa.name=art.name and sa.sampleid={sampleid};"

    return session.execute(text(query)).all()


def get_currentsteps_protocol_for_sample(session, sampleid):
    """returns the current protocolstep and if it is queued or worked on in that step for a sample

    :param session: the current SQLAlchemy session to the db
    :param sampleid: sampleid from sample table
    :returns: all protocolstep ids a sample is in and whether the sample is queued or worked on in that step
    """
    query = """
        SELECT DISTINCT
            COALESCE(stg.stepid, sc.stepid) AS stepid,
            CASE
                WHEN sc.stepid IS NOT NULL AND stg.stepid IS NULL THEN 'in-step'
                WHEN sc.stepid IS NULL AND stg.stepid IS NOT NULL THEN 'queued'
                WHEN stg.stepid IS NOT NULL AND sc.stepid IS NOT NULL THEN
                CASE
                    WHEN stg.stepid <> sc.stepid THEN 'queued'
                    ELSE 'in-step'
                END
                ELSE 'unknown'
            END AS status
        FROM stage stg
        JOIN stagetransition st ON stg.stageid = st.stageid
        JOIN artifact_sample_map asm ON asm.artifactid = st.artifactid
        JOIN sample sa ON sa.processid = asm.processid
        LEFT JOIN samplecheckout sc ON sc.artifactid = asm.artifactid
        WHERE st.workflowrunid > 0
          AND (stg.stepid IS NOT NULL OR sc.stepid IS NOT NULL)
          AND sa.sampleid = :sampleid;
    """

    # Execute query with parameterized sampleid
    return session.execute(text(query), {'sampleid': sampleid}).all()


def get_protocolstep_details(session, stepid):
    """returns the name of the protocolstep

    :param session: the current SQLAlchemy session to the db
    :param stepid: the id of the protocolstep
    :returns: protocolstep name
    """
    query = f"select ps.name, lp.protocolname, lp.qcprotocol \
              from protocolstep ps, labprotocol lp \
              where ps.protocolid=lp.protocolid and ps.stepid={stepid};"

    return session.execute(text(query)).all()
