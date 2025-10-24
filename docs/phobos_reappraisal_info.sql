--
-- PostgreSQL database dump
--

\restrict DuL05RGlYiYZuQIJH8Ic5Elt52LRImRFR1bSSmRBjTsuTxztbpnSLWweORIaTp8

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

--
-- Name: genderenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.genderenum AS ENUM (
    'MALE',
    'FEMALE',
    'OTHER'
);


ALTER TYPE public.genderenum OWNER TO postgres;

--
-- Name: reappraisalservicecategoryenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.reappraisalservicecategoryenum AS ENUM (
    'FOOD',
    'TRAVEL',
    'STAY',
    'MISC'
);


ALTER TYPE public.reappraisalservicecategoryenum OWNER TO postgres;

--
-- Name: reappraisalservicestatusenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.reappraisalservicestatusenum AS ENUM (
    'ACTIVE',
    'QUEUED',
    'CONSOLIDATED',
    'CLOSED'
);


ALTER TYPE public.reappraisalservicestatusenum OWNER TO postgres;

--
-- Name: settlementstatusenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.settlementstatusenum AS ENUM (
    'UNSETTLED',
    'CARRY_FORWARD',
    'SETTLED',
    'WRITTEN_OFF'
);


ALTER TYPE public.settlementstatusenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: advance_settlement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.advance_settlement (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    rsa_id character varying(36) NOT NULL,
    pst_id character varying(36) NOT NULL,
    rsca_status public.settlementstatusenum
);


ALTER TABLE public.advance_settlement OWNER TO postgres;

--
-- Name: appraiser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appraiser (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    ap_id character varying(36) NOT NULL,
    ap_first_name character varying(50),
    ap_last_name character varying(50),
    ap_gender public.genderenum,
    ap_email character varying(50),
    ap_phone character varying(15),
    ap_adhaar character varying(12),
    ap_pan character varying(10),
    ap_account_number character varying(20),
    ap_account_ifsc_code character varying(11)
);


ALTER TABLE public.appraiser OWNER TO postgres;

--
-- Name: charge_settlement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.charge_settlement (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    rs_id character varying(36) NOT NULL,
    pst_id character varying(36) NOT NULL,
    rs_set_status public.settlementstatusenum
);


ALTER TABLE public.charge_settlement OWNER TO postgres;

--
-- Name: payout_cycle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payout_cycle (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    pcy_id character varying(36) NOT NULL,
    pcy_start_epoch integer,
    pcy_end_epoch integer
);


ALTER TABLE public.payout_cycle OWNER TO postgres;

--
-- Name: payout_statement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payout_statement (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    pst_id character varying(36) NOT NULL,
    pst_app_id character varying(36),
    pst_cyc_id character varying(36),
    pst_prev_st_id character varying(36),
    pst_prev_st_bal integer,
    pst_tot_reapp_ser_amt integer,
    pst_tot_adv_amt integer,
    pst_tot_reimb_amt integer,
    pst_tot_bal integer,
    pst_status public.settlementstatusenum
);


ALTER TABLE public.payout_statement OWNER TO postgres;

--
-- Name: reappraisal_service; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reappraisal_service (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    rs_id character varying(36) NOT NULL,
    ap_id character varying(36),
    rs_branch_id character varying(36),
    rs_start_epoch integer,
    rs_end_epoch integer,
    rs_packet_count integer,
    rs_charge integer NOT NULL,
    rs_status public.reappraisalservicestatusenum,
    rs_file_path character varying(255),
    rs_settlement_status public.settlementstatusenum
);


ALTER TABLE public.reappraisal_service OWNER TO postgres;

--
-- Name: reappraisal_service_advance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reappraisal_service_advance (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    rsa_id character varying(36) NOT NULL,
    rs_id character varying(36),
    rsa_transaction_epoch integer,
    rsa_category public.reappraisalservicecategoryenum,
    rsa_amount integer,
    rsa_description character varying(255),
    rsa_settlement_status public.settlementstatusenum
);


ALTER TABLE public.reappraisal_service_advance OWNER TO postgres;

--
-- Name: reappraisal_service_reimbursement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reappraisal_service_reimbursement (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    rsr_id character varying(36) NOT NULL,
    rs_id character varying(36),
    rsr_transaction_epoch integer,
    rsr_category public.reappraisalservicecategoryenum,
    rsr_details character varying(255),
    rsr_amount integer,
    rsr_file_path character varying(255),
    rsr_settlement_status public.settlementstatusenum
);


ALTER TABLE public.reappraisal_service_reimbursement OWNER TO postgres;

--
-- Name: reimbursement_settlement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reimbursement_settlement (
    created_at_epoch integer,
    updated_at_epoch integer,
    deleted_at_epoch integer,
    rsr_id character varying(36) NOT NULL,
    pst_id character varying(36) NOT NULL,
    reimb_set_status public.settlementstatusenum
);


ALTER TABLE public.reimbursement_settlement OWNER TO postgres;

--
-- Name: advance_settlement advance_settlement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.advance_settlement
    ADD CONSTRAINT advance_settlement_pkey PRIMARY KEY (rsa_id, pst_id);


--
-- Name: appraiser appraiser_ap_adhaar_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appraiser
    ADD CONSTRAINT appraiser_ap_adhaar_key UNIQUE (ap_adhaar);


--
-- Name: appraiser appraiser_ap_pan_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appraiser
    ADD CONSTRAINT appraiser_ap_pan_key UNIQUE (ap_pan);


--
-- Name: appraiser appraiser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appraiser
    ADD CONSTRAINT appraiser_pkey PRIMARY KEY (ap_id);


--
-- Name: charge_settlement charge_settlement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_settlement
    ADD CONSTRAINT charge_settlement_pkey PRIMARY KEY (rs_id, pst_id);


--
-- Name: payout_cycle payout_cycle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payout_cycle
    ADD CONSTRAINT payout_cycle_pkey PRIMARY KEY (pcy_id);


--
-- Name: payout_statement payout_statement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payout_statement
    ADD CONSTRAINT payout_statement_pkey PRIMARY KEY (pst_id);


--
-- Name: reappraisal_service_advance reappraisal_service_advance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reappraisal_service_advance
    ADD CONSTRAINT reappraisal_service_advance_pkey PRIMARY KEY (rsa_id);


--
-- Name: reappraisal_service reappraisal_service_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reappraisal_service
    ADD CONSTRAINT reappraisal_service_pkey PRIMARY KEY (rs_id);


--
-- Name: reappraisal_service_reimbursement reappraisal_service_reimbursement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reappraisal_service_reimbursement
    ADD CONSTRAINT reappraisal_service_reimbursement_pkey PRIMARY KEY (rsr_id);


--
-- Name: reimbursement_settlement reimbursement_settlement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reimbursement_settlement
    ADD CONSTRAINT reimbursement_settlement_pkey PRIMARY KEY (rsr_id, pst_id);


--
-- Name: ix_appraiser_ap_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_appraiser_ap_phone ON public.appraiser USING btree (ap_phone);


--
-- Name: ix_appraiser_fullname; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_appraiser_fullname ON public.appraiser USING btree (ap_first_name, ap_last_name);


--
-- Name: ix_payout_statement_pst_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payout_statement_pst_status ON public.payout_statement USING btree (pst_status);


--
-- Name: ix_reappraisal_service_advance_rsa_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reappraisal_service_advance_rsa_category ON public.reappraisal_service_advance USING btree (rsa_category);


--
-- Name: ix_reappraisal_service_advance_rsa_settlement_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reappraisal_service_advance_rsa_settlement_status ON public.reappraisal_service_advance USING btree (rsa_settlement_status);


--
-- Name: ix_reappraisal_service_reimbursement_rsr_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reappraisal_service_reimbursement_rsr_category ON public.reappraisal_service_reimbursement USING btree (rsr_category);


--
-- Name: ix_reappraisal_service_reimbursement_rsr_settlement_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reappraisal_service_reimbursement_rsr_settlement_status ON public.reappraisal_service_reimbursement USING btree (rsr_settlement_status);


--
-- Name: ix_reappraisal_service_rs_settlement_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reappraisal_service_rs_settlement_status ON public.reappraisal_service USING btree (rs_settlement_status);


--
-- Name: ix_reappraisal_service_rs_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reappraisal_service_rs_status ON public.reappraisal_service USING btree (rs_status);


--
-- Name: advance_settlement advance_settlement_pst_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.advance_settlement
    ADD CONSTRAINT advance_settlement_pst_id_fkey FOREIGN KEY (pst_id) REFERENCES public.payout_statement(pst_id);


--
-- Name: advance_settlement advance_settlement_rsa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.advance_settlement
    ADD CONSTRAINT advance_settlement_rsa_id_fkey FOREIGN KEY (rsa_id) REFERENCES public.reappraisal_service_advance(rsa_id);


--
-- Name: charge_settlement charge_settlement_pst_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_settlement
    ADD CONSTRAINT charge_settlement_pst_id_fkey FOREIGN KEY (pst_id) REFERENCES public.payout_statement(pst_id);


--
-- Name: charge_settlement charge_settlement_rs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_settlement
    ADD CONSTRAINT charge_settlement_rs_id_fkey FOREIGN KEY (rs_id) REFERENCES public.reappraisal_service(rs_id);


--
-- Name: payout_statement payout_statement_pst_app_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payout_statement
    ADD CONSTRAINT payout_statement_pst_app_id_fkey FOREIGN KEY (pst_app_id) REFERENCES public.appraiser(ap_id);


--
-- Name: payout_statement payout_statement_pst_cyc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payout_statement
    ADD CONSTRAINT payout_statement_pst_cyc_id_fkey FOREIGN KEY (pst_cyc_id) REFERENCES public.payout_cycle(pcy_id);


--
-- Name: payout_statement payout_statement_pst_prev_st_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payout_statement
    ADD CONSTRAINT payout_statement_pst_prev_st_id_fkey FOREIGN KEY (pst_prev_st_id) REFERENCES public.payout_statement(pst_id);


--
-- Name: reappraisal_service_advance reappraisal_service_advance_rs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reappraisal_service_advance
    ADD CONSTRAINT reappraisal_service_advance_rs_id_fkey FOREIGN KEY (rs_id) REFERENCES public.reappraisal_service(rs_id);


--
-- Name: reappraisal_service reappraisal_service_ap_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reappraisal_service
    ADD CONSTRAINT reappraisal_service_ap_id_fkey FOREIGN KEY (ap_id) REFERENCES public.appraiser(ap_id);


--
-- Name: reappraisal_service_reimbursement reappraisal_service_reimbursement_rs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reappraisal_service_reimbursement
    ADD CONSTRAINT reappraisal_service_reimbursement_rs_id_fkey FOREIGN KEY (rs_id) REFERENCES public.reappraisal_service(rs_id);


--
-- Name: reimbursement_settlement reimbursement_settlement_pst_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reimbursement_settlement
    ADD CONSTRAINT reimbursement_settlement_pst_id_fkey FOREIGN KEY (pst_id) REFERENCES public.payout_statement(pst_id);


--
-- Name: reimbursement_settlement reimbursement_settlement_rsr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reimbursement_settlement
    ADD CONSTRAINT reimbursement_settlement_rsr_id_fkey FOREIGN KEY (rsr_id) REFERENCES public.reappraisal_service_reimbursement(rsr_id);


--
-- PostgreSQL database dump complete
--

\unrestrict DuL05RGlYiYZuQIJH8Ic5Elt52LRImRFR1bSSmRBjTsuTxztbpnSLWweORIaTp8

