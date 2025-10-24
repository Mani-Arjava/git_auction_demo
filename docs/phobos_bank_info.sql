--
-- PostgreSQL database dump
--

\restrict Nmm8jZfEHbgpxtAnOvaLICw6e0Ey1NFigpNdCJjWtsj9xOWgCvpcoPXAeR12nP5

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bank; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    bk_id character varying(36) NOT NULL,
    bk_name character varying(50),
    bk_code character varying(5),
    total_branches_count character varying(10)
);


ALTER TABLE public.bank OWNER TO postgres;

--
-- Name: bank_employee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank_employee (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    bk_employee_id character varying(36) NOT NULL,
    bk_employee_first_name character varying(50),
    bk_employee_last_name character varying(50),
    bk_employee_email character varying(100),
    bk_employee_phone character varying(15),
    bk_employee_designation character varying(50)
);


ALTER TABLE public.bank_employee OWNER TO postgres;

--
-- Name: bank_employee_assignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank_employee_assignment (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    bk_employee_id character varying(36) NOT NULL,
    br_id character varying(36) NOT NULL
);


ALTER TABLE public.bank_employee_assignment OWNER TO postgres;

--
-- Name: branch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branch (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    br_id character varying(36) NOT NULL,
    br_bk_id character varying(36),
    br_name character varying(50),
    br_sol_id character varying(6),
    br_ifsc_code character varying(15),
    br_address_line1 character varying(500),
    br_address_line2 character varying(100),
    br_city character varying(50),
    br_state character varying(50),
    br_region character varying(50),
    br_postal_code character varying(10),
    br_latitude character varying(20),
    br_longitude character varying(20)
);


ALTER TABLE public.branch OWNER TO postgres;

--
-- Name: bank_employee_assignment bank_employee_assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_employee_assignment
    ADD CONSTRAINT bank_employee_assignment_pkey PRIMARY KEY (bk_employee_id, br_id);


--
-- Name: bank_employee bank_employee_bk_employee_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_employee
    ADD CONSTRAINT bank_employee_bk_employee_email_key UNIQUE (bk_employee_email);


--
-- Name: bank_employee bank_employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_employee
    ADD CONSTRAINT bank_employee_pkey PRIMARY KEY (bk_employee_id);


--
-- Name: bank bank_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank
    ADD CONSTRAINT bank_pkey PRIMARY KEY (bk_id);


--
-- Name: branch branch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch
    ADD CONSTRAINT branch_pkey PRIMARY KEY (br_id);


--
-- Name: ix_bank_bk_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_bank_bk_code ON public.bank USING btree (bk_code);


--
-- Name: ix_bank_bk_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_bank_bk_name ON public.bank USING btree (bk_name);


--
-- Name: ix_bank_total_branches_count; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_bank_total_branches_count ON public.bank USING btree (total_branches_count);


--
-- Name: ix_branch_br_city; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_city ON public.branch USING btree (br_city);


--
-- Name: ix_branch_br_ifsc_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_branch_br_ifsc_code ON public.branch USING btree (br_ifsc_code);


--
-- Name: ix_branch_br_latitude; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_latitude ON public.branch USING btree (br_latitude);


--
-- Name: ix_branch_br_longitude; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_longitude ON public.branch USING btree (br_longitude);


--
-- Name: ix_branch_br_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_name ON public.branch USING btree (br_name);


--
-- Name: ix_branch_br_postal_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_postal_code ON public.branch USING btree (br_postal_code);


--
-- Name: ix_branch_br_region; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_region ON public.branch USING btree (br_region);


--
-- Name: ix_branch_br_sol_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_sol_id ON public.branch USING btree (br_sol_id);


--
-- Name: ix_branch_br_state; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_branch_br_state ON public.branch USING btree (br_state);


--
-- Name: bank_employee_assignment bank_employee_assignment_bk_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_employee_assignment
    ADD CONSTRAINT bank_employee_assignment_bk_employee_id_fkey FOREIGN KEY (bk_employee_id) REFERENCES public.bank_employee(bk_employee_id);


--
-- Name: bank_employee_assignment bank_employee_assignment_br_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_employee_assignment
    ADD CONSTRAINT bank_employee_assignment_br_id_fkey FOREIGN KEY (br_id) REFERENCES public.branch(br_id);


--
-- Name: branch branch_br_bk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch
    ADD CONSTRAINT branch_br_bk_id_fkey FOREIGN KEY (br_bk_id) REFERENCES public.bank(bk_id);


--
-- PostgreSQL database dump complete
--

\unrestrict Nmm8jZfEHbgpxtAnOvaLICw6e0Ey1NFigpNdCJjWtsj9xOWgCvpcoPXAeR12nP5

