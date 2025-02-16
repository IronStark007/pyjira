from pyjira.actions import task


class TestTask:
    def test_add_task_success(self, db_session, add_task_data):
        """
        GIVEN there does not exist a task with same title
        WHEN add_task method is called
        THEN it creates the task
        """
        # GIVEN
        payload = add_task_data.get("payload")
        expected_response = add_task_data.get("expected_response")
        # WHEN
        actual_response = task.add_task(data=payload, session=db_session)
        # THEN
        assert actual_response.title == expected_response.title
        assert actual_response.description == expected_response.description
        assert actual_response.completed == expected_response.completed

    def test_add_task_failure(self, db_session, add_task_data, caplog):
        """
        GIVEN there exist a task with same title
        WHEN add_task method is called
        THEN it logs the error
        """
        # GIVEN
        payload = add_task_data.get("payload")
        error_response = add_task_data.get("error_response")
        task.add_task(data=payload, session=db_session)
        # WHEN
        task.add_task(data=payload, session=db_session)
        # THEN
        assert any(error_response == message for message in caplog.messages)

    def test_list_task_with_task(self, db_session, list_task_data):
        """
        GIVEN there exist some task in db
        WHEN list_task method is called
        THEN return the list of tasks
        """
        # GIVEN
        payload = list_task_data.get("payload")
        expected_response = list_task_data.get("expected_response")
        for data in payload:
            task.add_task(data=data, session=db_session)
        # WHEN
        actual_response = task.list_tasks(session=db_session)
        # THEN
        for actual, expected in zip(actual_response, expected_response):
            assert actual.title == expected.title
            assert actual.description == expected.description
            assert actual.completed == expected.completed

    def test_list_task_with_no_task(self, db_session, list_task_data, caplog):
        """
        GIVEN there does not exists task in db
        WHEN list_task method is called
        THEN it returns None
        """
        # GIVEN
        error_response = list_task_data.get("error_response")
        # WHEN
        actual_response = task.list_tasks(session=db_session)
        # THEN
        assert actual_response is None
        assert any(error_response == message for message in caplog.messages)

    def test_mark_complete_success(self, db_session, update_task_data):
        """
        GIVEN there exist a task in db
        WHEN mark_complete method is called
        THEN it mark the task as completed
        """
        # GIVEN
        add_payload = update_task_data.get("add_payload")
        update_payload = update_task_data.get("update_payload")
        expected_response = update_task_data.get("expected_response")
        task.add_task(data=add_payload, session=db_session)
        # WHEN
        actual_response = task.mark_complete(data=update_payload, session=db_session)
        # THEN
        assert actual_response.title == expected_response.title
        assert actual_response.description == expected_response.description
        assert actual_response.completed == expected_response.completed

    def test_mark_complete_failure(self, db_session, update_task_data, caplog):
        """
        GIVEN there does not exist a task in db
        WHEN mark_complete method is called
        THEN it logs the error
        """
        # GIVEN
        update_payload = update_task_data.get("update_payload")
        error_response = update_task_data.get("error_response")
        # WHEN
        task.mark_complete(data=update_payload, session=db_session)
        # THEN
        assert any(error_response == message for message in caplog.messages)

    def test_delete_task_success(self, db_session, delete_task_data, caplog):
        """
        GIVEN there exist a task in db
        WHEN delete_task method is called
        THEN it deletes the task and logs the response
        """
        # GIVEN
        payload = delete_task_data.get("add_payload")
        expected_response = delete_task_data.get("expected_response")
        task.add_task(data=payload, session=db_session)
        # WHEN
        task.delete_task(task_title=payload.get("title"), session=db_session)
        # THEN
        assert any(expected_response == message for message in caplog.messages)

    def test_delete_task_failure(self, db_session, delete_task_data, caplog):
        """
        GIVEN there does not exist a task in db
        WHEN delete_task method is called
        THEN it logs the error
        """
        # GIVEN
        payload = delete_task_data.get("add_payload")
        error_response = delete_task_data.get("error_response")
        # WHEN
        task.delete_task(task_title=payload.get("title"), session=db_session)
        # THEN
        assert any(error_response == message for message in caplog.messages)
